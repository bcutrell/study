use anyhow::Result;
use reggr::Config;
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use tempfile::{NamedTempFile, TempDir};

// Config Tests
#[test]
fn test_config_from_file() -> Result<()> {
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

    let mut temp_file = NamedTempFile::new()?;
    write!(temp_file, "{}", config_content)?;

    let expected_config: Config = toml::from_str(config_content)?;
    let config = Config::from_file(&temp_file.path().to_path_buf())?;

    assert_eq!(config.old_cmd, expected_config.old_cmd);
    assert_eq!(config.new_cmd, expected_config.new_cmd);
    assert_eq!(config.input_dir, expected_config.input_dir);

    Ok(())
}

#[test]
fn test_config_from_cli() {
    let config = Config::from_cli_args(
        "old.py",
        "new.py",
        &PathBuf::from("input/"),
        &PathBuf::from("output/"),
        Some("-i {input} -o {output}".to_string()),
        Some("-i {input} -o {output}".to_string()),
        Some(false),
    );

    assert_eq!(config.old_cmd, "old.py");
    assert_eq!(config.new_cmd, "new.py");
    assert_eq!(config.input_dir, PathBuf::from("input/"));
    assert_eq!(config.output_dir, PathBuf::from("output/"));
    assert_eq!(config.concurrent, false);
}

#[test]
fn test_config_merge() {
    let mut config = Config::from_cli_args(
        "old.py",
        "new.py",
        &PathBuf::from("input/"),
        &PathBuf::from("output/"),
        None,
        None,
        None,
    );

    let new_old_cmd = "new_old.py".to_string();
    let new_input_dir = PathBuf::from("new_input/");

    config = config.merge_cli_args(
        Some(&new_old_cmd),
        None,
        Some(&new_input_dir),
        None,
        None,
        None,
        None,
    );

    assert_eq!(config.old_cmd, "new_old.py");
    assert_eq!(config.new_cmd, "new.py");
    assert_eq!(config.input_dir, PathBuf::from("new_input/"));
    assert_eq!(config.output_dir, PathBuf::from("output/"));
}

// Execution Tests
#[test]
fn test_execute_sequential() -> Result<()> {
    let input_dir = TempDir::new()?;
    let output_dir = TempDir::new()?;

    // Create test input file
    let input_path = input_dir.path().join("test_input.txt");
    File::create(&input_path)?.write_all(b"test content")?;

    // Create test script
    let script_content = r#"#!/bin/sh
echo "Input: $1"
echo "Output: $2"
"#;
    let script_path = input_dir.path().join("test_script.sh");
    File::create(&script_path)?.write_all(script_content.as_bytes())?;

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
        concurrent: false,
    };

    reggr::execute_sequential(&config)?;

    // Verify outputs
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
