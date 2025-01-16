use clap::Parser;
use std::error::Error;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// First script/executable to test
    #[arg(short = 'a', long)]
    script_a: String,

    /// Second script/executable to test
    #[arg(short = 'b', long)]
    script_b: String,

    /// Directory containing input files
    #[arg(short = 'i', long)]
    input_dir: String,

    /// Working directory for outputs
    #[arg(short = 'w', long)]
    work_dir: String,
}

fn run_single_test(
    script_path: &Path,
    input_file: &Path,
    output_file: &Path,
) -> Result<(), Box<dyn Error>> {
    // Check if script exists
    if !script_path.exists() {
        return Err(format!("Script not found: {}", script_path.display()).into());
    }

    // Check if input file exists
    if !input_file.exists() {
        return Err(format!("Input file not found: {}", input_file.display()).into());
    }

    let extension = script_path.extension().and_then(|e| e.to_str());

    let output = match extension {
        Some("py") => Command::new("python")
            .arg(script_path)
            .args(["-i", input_file.to_str().unwrap()])
            .args(["-o", output_file.to_str().unwrap()])
            .output()
            .map_err(|e| {
                format!(
                    "Failed to execute Python script {}: {}",
                    script_path.display(),
                    e
                )
            })?,
        Some("exe") | None => {
            // For executables, first check if the file exists and is executable
            if !script_path.exists() {
                return Err(format!("Executable not found: {}", script_path.display()).into());
            }

            // Make a copy of PathBuf for modification if needed
            let exec_path = if cfg!(windows) {
                // On Windows, try with and without .exe
                let mut path = script_path.to_path_buf();
                if path.extension().is_none() {
                    path.set_extension("exe");
                }
                path
            } else {
                script_path.to_path_buf()
            };

            Command::new(&exec_path)
                .args(["-i", input_file.to_str().unwrap()])
                .args(["-o", output_file.to_str().unwrap()])
                .output()
                .map_err(|e| format!("Failed to execute {}: {}", exec_path.display(), e))?
        }
        _ => return Err(format!("Unsupported script type: {}", script_path.display()).into()),
    };

    if !output.status.success() {
        return Err(format!("Script failed: {}", String::from_utf8_lossy(&output.stderr)).into());
    }

    Ok(())
}

fn setup_workspace(work_dir: &Path) -> Result<(), Box<dyn Error>> {
    fs::create_dir_all(work_dir).map_err(|e| {
        format!(
            "Failed to create working directory {}: {}",
            work_dir.display(),
            e
        )
    })?;
    fs::create_dir_all(work_dir.join("script_a"))
        .map_err(|e| format!("Failed to create script_a output directory: {}", e))?;
    fs::create_dir_all(work_dir.join("script_b"))
        .map_err(|e| format!("Failed to create script_b output directory: {}", e))?;
    Ok(())
}

fn get_input_files(input_dir: &Path) -> Result<Vec<PathBuf>, Box<dyn Error>> {
    if !input_dir.exists() {
        return Err(format!("Input directory not found: {}", input_dir.display()).into());
    }

    let files: Vec<_> = fs::read_dir(input_dir)
        .map_err(|e| {
            format!(
                "Failed to read input directory {}: {}",
                input_dir.display(),
                e
            )
        })?
        .filter_map(|entry| entry.ok())
        .map(|entry| entry.path())
        .collect();

    if files.is_empty() {
        return Err(format!("No input files found in directory: {}", input_dir.display()).into());
    }

    Ok(files)
}

fn run_tests(args: Args) -> Result<(), Box<dyn Error>> {
    let work_dir = PathBuf::from(&args.work_dir);
    let input_dir = PathBuf::from(&args.input_dir);

    setup_workspace(&work_dir)?;

    // Get and validate input files
    let input_files = get_input_files(&input_dir)?;

    // Run tests for script A
    println!("Running tests for script A...");
    for (i, input_file) in input_files.iter().enumerate() {
        let output_file = work_dir
            .join("script_a")
            .join(format!("output_{}.txt", i + 1));
        run_single_test(Path::new(&args.script_a), input_file, &output_file)?;
    }

    // Run tests for script B
    println!("Running tests for script B...");
    for (i, input_file) in input_files.iter().enumerate() {
        let output_file = work_dir
            .join("script_b")
            .join(format!("output_{}.txt", i + 1));
        run_single_test(Path::new(&args.script_b), input_file, &output_file)?;
    }

    println!("All tests completed successfully");
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    run_tests(args)
}
