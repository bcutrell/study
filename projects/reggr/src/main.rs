use anyhow::{Context, Result};
use clap::Parser;
use serde_derive::Deserialize;
use std::fs::{self, read_dir};
use std::path::Path;
use std::path::PathBuf;
use std::process::Command;

#[derive(Debug, Clone, Deserialize)]
struct Config {
    preprocess: Option<String>,
    old_cmd: String,
    old_cmd_args: Option<String>,
    new_cmd: String,
    new_cmd_args: Option<String>,
    input_dir: PathBuf,
    output_dir: PathBuf,
    postprocess: Option<String>,
}

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to config file
    #[arg(short, long)]
    config: Option<PathBuf>,

    /// Optional preprocessing script to run before tests
    #[arg(long)]
    preprocess: Option<String>,

    /// Old command/script to test
    #[arg(long)]
    old_cmd: Option<String>,

    /// Arguments for old command
    #[arg(long, allow_hyphen_values = true)]
    old_cmd_args: Option<String>,

    /// New command/script to test
    #[arg(long)]
    new_cmd: Option<String>,

    /// Arguments for new command
    #[arg(long, allow_hyphen_values = true)]
    new_cmd_args: Option<String>,

    // TODO: Fixed Arguments for both old and new commands
    // #[arg(long, allow_hyphen_values = true)]
    // cmd_args: Option<String>,
    /// Input directory containing test files
    #[arg(long)]
    input_dir: Option<PathBuf>,

    /// Optional postprocessing script to run after tests
    #[arg(long)]
    postprocess: Option<String>,

    /// Output directory for results
    #[arg(long)]
    output_dir: Option<PathBuf>,
}

impl Config {
    fn from_file(path: &PathBuf) -> Result<Self> {
        let content = std::fs::read_to_string(path)
            .with_context(|| format!("Failed to read config file: {}", path.display()))?;
        let config: Config = toml::from_str(&content)
            .with_context(|| format!("Failed to parse config file: {}", path.display()))?;
        Ok(config)
    }

    fn from_cli_args(args: &Args) -> Result<Self> {
        let old_cmd = args
            .old_cmd
            .as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --old_cmd"))?;
        let new_cmd = args
            .new_cmd
            .as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --new_cmd"))?;
        let input_dir = args
            .input_dir
            .as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --input-dir"))?;
        let output_dir = args
            .output_dir
            .as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --output-dir"))?;

        Ok(Config {
            preprocess: None,
            old_cmd: old_cmd.clone(),
            old_cmd_args: args.old_cmd_args.clone(),
            new_cmd: new_cmd.clone(),
            new_cmd_args: args.new_cmd_args.clone(),
            input_dir: input_dir.clone(),
            output_dir: output_dir.clone(),
            postprocess: None,
        })
    }

    fn merge_cli_args(mut self, args: &Args) -> Self {
        if let Some(old_cmd) = &args.old_cmd {
            self.old_cmd = old_cmd.clone();
        }
        if let Some(old_cmd_args) = &args.old_cmd_args {
            self.old_cmd_args = Some(old_cmd_args.clone());
        }
        if let Some(new_cmd) = &args.new_cmd {
            self.new_cmd = new_cmd.clone();
        }
        if let Some(new_cmd_args) = &args.new_cmd_args {
            self.new_cmd_args = Some(new_cmd_args.clone());
        }
        if let Some(input_dir) = &args.input_dir {
            self.input_dir = input_dir.clone();
        }
        if let Some(output_dir) = &args.output_dir {
            self.output_dir = output_dir.clone();
        }
        self
    }

    fn validate(&self) -> Result<()> {
        // Placeholder for validation logic
        Ok(())
    }
}

fn get_config(args: &Args) -> Result<Config> {
    let config = if let Some(config_path) = &args.config {
        // Read from config file
        let mut config = Config::from_file(config_path)?;

        // If CLI args are also present, merge them with precedence
        if args.old_cmd.is_some()
            || args.new_cmd.is_some()
            || args.input_dir.is_some()
            || args.output_dir.is_some()
        {
            println!("Note: CLI arguments will override config file values where present");
            config = config.merge_cli_args(args);
        }
        config
    } else {
        // Use only CLI arguments
        Config::from_cli_args(args)?
    };

    config.validate()?;
    Ok(config)
}

fn execute_sequential(config: &Config) -> Result<()> {
    // Create output directory if it doesn't exist
    fs::create_dir_all(&config.output_dir)?;

    // Get all files from input directory
    let input_files = read_dir(&config.input_dir).with_context(|| {
        format!(
            "Failed to read input directory: {}",
            config.input_dir.display()
        )
    })?;

    // Execute commands for each input file
    for file in input_files {
        let file = file?;
        let input_path = file.path();
        if !input_path.is_file() {
            continue;
        }
        let file_stem = input_path
            .file_stem()
            .and_then(|s| s.to_str())
            .ok_or_else(|| anyhow::anyhow!("Invalid input filename"))?;

        println!("Processing file: {}", file_stem);

        // Old command
        let old_output_path = config.output_dir.join(format!("{}_old.txt", file_stem));
        execute_command(
            &config.old_cmd,
            &config.old_cmd_args,
            &input_path,
            &old_output_path,
        )?;

        // New command
        let new_output_path = config.output_dir.join(format!("{}_new.txt", file_stem));
        execute_command(
            &config.new_cmd,
            &config.new_cmd_args,
            &input_path,
            &new_output_path,
        )?;
    }

    Ok(())
}

fn execute_command(
    cmd: &str,
    args: &Option<String>,
    input_path: &Path,
    output_path: &Path,
) -> Result<()> {
    // Build command with arguments
    let cmd_parts: Vec<&str> = cmd.split_whitespace().collect();
    if cmd_parts.is_empty() {
        return Err(anyhow::anyhow!("Empty command"));
    }

    // Command
    let program = cmd_parts[0];
    let mut command = Command::new(program);

    // Arguments
    if cmd_parts.len() > 1 {
        command.args(&cmd_parts[1..]);
    }

    if let Some(args) = args {
        // Replace placeholders in arguments with actual paths
        let args = args
            .replace("{input}", input_path.to_str().unwrap())
            .replace("{output}", output_path.to_str().unwrap());

        // Split args string into individual arguments
        command.args(args.split_whitespace());

        println!("Executing: {} {}", cmd, args);
    } else {
        println!("Executing: {}", cmd);
    }

    // Execute command and capture output
    let output = command
        .output()
        .with_context(|| format!("Failed to execute command: {}", cmd))?;

    // Write command output and metadata to file
    let mut content = String::new();
    content.push_str(&format!("exit_status: {}\n", output.status));
    content.push_str("---stdout---\n");
    content.push_str(&String::from_utf8_lossy(&output.stdout));
    content.push_str("\n---stderr---\n");
    content.push_str(&String::from_utf8_lossy(&output.stderr));

    fs::write(output_path, content)
        .with_context(|| format!("Failed to write output to: {}", output_path.display()))?;

    if !output.status.success() {
        println!(
            "Warning: Command '{}' failed with status: {}",
            cmd, output.status
        );
    }

    Ok(())
}

fn main() -> Result<()> {
    let args = Args::parse();
    let config = get_config(&args)?;

    println!("Configuration:");
    println!("  Old command: {}", config.old_cmd);
    println!("  Old command args: {:?}", config.old_cmd_args);
    println!("  New command: {}", config.new_cmd);
    println!("  New command args: {:?}", config.new_cmd_args);
    println!("  Input directory: {}", config.input_dir.display());
    println!("  Output directory: {}", config.output_dir.display());
    println!("  Preprocess script: {:?}", config.preprocess);
    println!("  Postprocess script: {:?}", config.postprocess);

    execute_sequential(&config)?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Ok;
    use std::fs::File;
    use std::io::Write;
    use tempfile::NamedTempFile;
    use tempfile::TempDir;

    fn create_test_config() -> (NamedTempFile, Config) {
        let config_content = r#"
            old_cmd = "script_a.py"
            old_cmd_args = "-i input.txt -o output.txt"
            new_cmd = "script_b.py"
            new_cmd_args = "-i input.txt -o output.txt"
            input_dir = "inputs/"
            output_dir = "outputs/"
            preprocess = "preprocess.sh"
            postprocess = "postprocess.sh"
        "#;

        let mut temp_file = NamedTempFile::new().unwrap();
        write!(temp_file, "{}", config_content).unwrap();

        let config: Config = toml::from_str(config_content).unwrap();
        (temp_file, config)
    }

    #[test]
    fn test_config_file_parsing() -> Result<()> {
        let (temp_file, expected_config) = create_test_config();
        let config = Config::from_file(&temp_file.path().to_path_buf())?;

        assert_eq!(config.old_cmd, expected_config.old_cmd);
        assert_eq!(config.old_cmd_args, expected_config.old_cmd_args);
        assert_eq!(config.new_cmd, expected_config.new_cmd);
        assert_eq!(config.input_dir, expected_config.input_dir);
        assert_eq!(config.output_dir, expected_config.output_dir);
        assert_eq!(config.preprocess, expected_config.preprocess);
        assert_eq!(config.postprocess, expected_config.postprocess);

        Ok(())
    }

    #[test]
    fn test_cli_override_config() -> Result<()> {
        let (temp_file, _) = create_test_config();

        let args = Args {
            config: Some(temp_file.path().to_path_buf()),
            preprocess: None,
            old_cmd: Some("new_script_a.py".to_string()),
            old_cmd_args: None,
            new_cmd: Some("new_script_b.py".to_string()),
            new_cmd_args: None,
            input_dir: Some(PathBuf::from("new_inputs/")),
            output_dir: None,
            postprocess: None,
        };

        let config = get_config(&args)?;

        assert_eq!(config.old_cmd, "new_script_a.py");
        assert_eq!(config.new_cmd, "new_script_b.py");
        assert_eq!(config.input_dir, PathBuf::from("new_inputs/"));
        assert_eq!(config.output_dir, PathBuf::from("outputs/")); // From config file

        Ok(())
    }

    #[test]
    fn test_cli_only() -> Result<()> {
        let args = Args {
            config: None,
            preprocess: None,
            old_cmd: Some("script_a.py".to_string()),
            old_cmd_args: None,
            new_cmd: Some("script_b.py".to_string()),
            new_cmd_args: None,
            input_dir: Some(PathBuf::from("inputs/")),
            output_dir: Some(PathBuf::from("outputs/")),
            postprocess: None,
        };

        let config = get_config(&args)?;

        assert_eq!(config.old_cmd, "script_a.py");
        assert_eq!(config.new_cmd, "script_b.py");
        assert_eq!(config.input_dir, PathBuf::from("inputs/"));
        assert_eq!(config.output_dir, PathBuf::from("outputs/"));
        assert_eq!(config.preprocess, None);
        assert_eq!(config.postprocess, None);

        Ok(())
    }

    #[test]
    #[should_panic(expected = "Missing required argument")]
    fn test_cli_missing_required_args() {
        let args = Args {
            config: None,
            preprocess: None,
            old_cmd: Some("script_a.py".to_string()),
            old_cmd_args: None,
            new_cmd: None, // Missing required argument
            new_cmd_args: None,
            input_dir: Some(PathBuf::from("inputs/")),
            output_dir: Some(PathBuf::from("outputs/")),
            postprocess: None,
        };

        get_config(&args).unwrap();
    }

    #[test]
    fn test_execute_sequential() -> Result<()> {
        // Create temporary directories for input and output
        let input_dir = TempDir::new()?;
        let output_dir = TempDir::new()?;

        // Create a test input file
        let input_path = input_dir.path().join("test_input.txt");
        File::create(&input_path)?.write_all(b"test content")?;

        // Create a simple echo script for testing
        let script_content = r#"#!/bin/sh
echo "Input: $1"
echo "Output: $2"
"#;
        let script_path = input_dir.path().join("test_script.sh");
        File::create(&script_path)?.write_all(script_content.as_bytes())?;
        // Make the script executable
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            let mut perms = fs::metadata(&script_path)?.permissions();
            perms.set_mode(0o755);
            fs::set_permissions(&script_path, perms)?;
        }

        let config = Config {
            preprocess: None,
            old_cmd: script_path.to_str().unwrap().to_string(),
            old_cmd_args: Some("{input} {output}".to_string()),
            new_cmd: script_path.to_str().unwrap().to_string(),
            new_cmd_args: Some("{input} {output}".to_string()),
            input_dir: input_dir.path().to_path_buf(),
            output_dir: output_dir.path().to_path_buf(),
            postprocess: None,
        };

        execute_sequential(&config)?;

        // Verify output files were created
        let old_output = output_dir.path().join("test_input_old.txt");
        let new_output = output_dir.path().join("test_input_new.txt");

        assert!(old_output.exists());
        assert!(new_output.exists());

        // Verify output content
        let old_content = fs::read_to_string(&old_output)?;
        let new_content = fs::read_to_string(&new_output)?;

        assert!(old_content.contains("Input:"));
        assert!(old_content.contains("Output:"));
        assert!(new_content.contains("Input:"));
        assert!(new_content.contains("Output:"));

        Ok(())
    }
}
