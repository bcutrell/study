use anyhow::{Context, Result};
use serde_derive::Deserialize;
use std::fs::{self, read_dir};
use std::path::{Path, PathBuf};
use std::process::Command;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub preprocess: Option<String>,
    pub old_cmd: String,
    pub old_cmd_args: Option<String>,
    pub new_cmd: String,
    pub new_cmd_args: Option<String>,
    pub input_dir: PathBuf,
    pub output_dir: PathBuf,
    pub postprocess: Option<String>,
}

impl Config {
    pub fn from_file(path: &PathBuf) -> Result<Self> {
        let content = std::fs::read_to_string(path)
            .with_context(|| format!("Failed to read config file: {}", path.display()))?;
        let config: Config = toml::from_str(&content)
            .with_context(|| format!("Failed to parse config file: {}", path.display()))?;
        Ok(config)
    }

    pub fn from_cli_args(
        old_cmd: &str,
        new_cmd: &str,
        input_dir: &PathBuf,
        output_dir: &PathBuf,
        old_cmd_args: Option<String>,
        new_cmd_args: Option<String>,
    ) -> Self {
        Config {
            preprocess: None,
            old_cmd: old_cmd.to_string(),
            old_cmd_args,
            new_cmd: new_cmd.to_string(),
            new_cmd_args,
            input_dir: input_dir.clone(),
            output_dir: output_dir.clone(),
            postprocess: None,
        }
    }

    pub fn merge_cli_args(
        mut self,
        old_cmd: Option<&String>,
        new_cmd: Option<&String>,
        input_dir: Option<&PathBuf>,
        output_dir: Option<&PathBuf>,
        old_cmd_args: Option<&String>,
        new_cmd_args: Option<&String>,
    ) -> Self {
        if let Some(old_cmd) = old_cmd {
            self.old_cmd = old_cmd.clone();
        }
        if let Some(old_cmd_args) = old_cmd_args {
            self.old_cmd_args = Some(old_cmd_args.clone());
        }
        if let Some(new_cmd) = new_cmd {
            self.new_cmd = new_cmd.clone();
        }
        if let Some(new_cmd_args) = new_cmd_args {
            self.new_cmd_args = Some(new_cmd_args.clone());
        }
        if let Some(input_dir) = input_dir {
            self.input_dir = input_dir.clone();
        }
        if let Some(output_dir) = output_dir {
            self.output_dir = output_dir.clone();
        }
        self
    }

    pub fn validate(&self) -> Result<()> {
        Ok(())
    }
}

pub fn execute_sequential(config: &Config) -> Result<()> {
    fs::create_dir_all(&config.output_dir)?;

    let input_files = read_dir(&config.input_dir).with_context(|| {
        format!(
            "Failed to read input directory: {}",
            config.input_dir.display()
        )
    })?;

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

        let old_output_path = config.output_dir.join(format!("{}_old.txt", file_stem));
        execute_command(
            &config.old_cmd,
            &config.old_cmd_args,
            &input_path,
            &old_output_path,
        )?;

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
    let cmd_parts: Vec<&str> = cmd.split_whitespace().collect();
    if cmd_parts.is_empty() {
        return Err(anyhow::anyhow!("Empty command"));
    }

    let program = cmd_parts[0];
    let mut command = Command::new(program);

    if cmd_parts.len() > 1 {
        command.args(&cmd_parts[1..]);
    }

    if let Some(args) = args {
        let args = args
            .replace("{input}", input_path.to_str().unwrap())
            .replace("{output}", output_path.to_str().unwrap());

        command.args(args.split_whitespace());
        println!("Executing: {} {}", cmd, args);
    } else {
        println!("Executing: {}", cmd);
    }

    let output = command
        .output()
        .with_context(|| format!("Failed to execute command: {}", cmd))?;

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