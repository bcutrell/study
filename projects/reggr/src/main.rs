use anyhow::{Context, Result};
use clap::Parser;
use serde_derive::Deserialize;
use std::path::PathBuf;

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

    /// Old command/script to test
    #[arg(long)]
    old_cmd: Option<String>,

    /// New command/script to test
    #[arg(long)]
    new_cmd: Option<String>,

    /// Input directory containing test files
    #[arg(long)]
    input_dir: Option<PathBuf>,

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
        let old_cmd = args.old_cmd.as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --old_cmd"))?;
        let new_cmd = args.new_cmd.as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --new_cmd"))?;
        let input_dir = args.input_dir.as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --input-dir"))?;
        let output_dir = args.output_dir.as_ref()
            .ok_or_else(|| anyhow::anyhow!("Missing required argument: --output-dir"))?;

        Ok(Config {
            preprocess: None,
            old_cmd: old_cmd.clone(),
            old_cmd_args: None,
            new_cmd: new_cmd.clone(),
            new_cmd_args: None,
            input_dir: input_dir.clone(),
            output_dir: output_dir.clone(),
            postprocess: None,
        })
    }

    fn merge_cli_args(mut self, args: &Args) -> Self {
        if let Some(old_cmd) = &args.old_cmd {
            self.old_cmd = old_cmd.clone();
        }
        if let Some(new_cmd) = &args.new_cmd {
            self.new_cmd = new_cmd.clone();
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
        // Add validation logic here if needed
        Ok(())
    }
}

fn get_config(args: &Args) -> Result<Config> {
    let config = if let Some(config_path) = &args.config {
        // Read from config file
        let mut config = Config::from_file(config_path)?;
        
        // If CLI args are also present, merge them with precedence
        if args.old_cmd.is_some() || args.new_cmd.is_some() || 
           args.input_dir.is_some() || args.output_dir.is_some() {
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

fn main() -> Result<()> {
    let args = Args::parse();
    let config = get_config(&args)?;

    println!("Final configuration:");
    println!("  Old command: {}", config.old_cmd);
    println!("  Old command args: {:?}", config.old_cmd_args);
    println!("  New command: {}", config.new_cmd);
    println!("  New command args: {:?}", config.new_cmd_args);
    println!("  Input directory: {}", config.input_dir.display());
    println!("  Output directory: {}", config.output_dir.display());
    println!("  Preprocess script: {:?}", config.preprocess);
    println!("  Postprocess script: {:?}", config.postprocess);

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

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
            old_cmd: Some("new_script_a.py".to_string()),
            new_cmd: Some("new_script_b.py".to_string()),
            input_dir: Some(PathBuf::from("new_inputs/")),
            output_dir: None,
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
            old_cmd: Some("script_a.py".to_string()),
            new_cmd: Some("script_b.py".to_string()),
            input_dir: Some(PathBuf::from("inputs/")),
            output_dir: Some(PathBuf::from("outputs/")),
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
            old_cmd: Some("script_a.py".to_string()),
            new_cmd: None, // Missing required argument
            input_dir: Some(PathBuf::from("inputs/")),
            output_dir: Some(PathBuf::from("outputs/")),
        };

        get_config(&args).unwrap();
    }
}