use anyhow::Result;
use clap::Parser;
use std::path::PathBuf;
use tokio;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    config: Option<PathBuf>,

    #[arg(long)]
    preprocess: Option<String>,

    #[arg(long)]
    old_cmd: Option<String>,

    #[arg(long, allow_hyphen_values = true)]
    old_cmd_args: Option<String>,

    #[arg(long)]
    new_cmd: Option<String>,

    #[arg(long, allow_hyphen_values = true)]
    new_cmd_args: Option<String>,

    #[arg(long)]
    input_dir: Option<PathBuf>,

    #[arg(long)]
    postprocess: Option<String>,

    #[arg(long)]
    output_dir: Option<PathBuf>,

    #[arg(long)]
    concurrent: bool,
}

fn get_config(args: &Args) -> Result<reggr::Config> {
    let config = if let Some(config_path) = &args.config {
        let mut config = reggr::Config::from_file(config_path)?;

        if args.old_cmd.is_some()
            || args.new_cmd.is_some()
            || args.input_dir.is_some()
            || args.output_dir.is_some()
        {
            println!("Note: CLI arguments will override config file values where present");
            config = config.merge_cli_args(
                args.old_cmd.as_ref(),
                args.new_cmd.as_ref(),
                args.input_dir.as_ref(),
                args.output_dir.as_ref(),
                args.old_cmd_args.as_ref(),
                args.new_cmd_args.as_ref(),
            );
        }
        config
    } else {
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

        reggr::Config::from_cli_args(
            old_cmd,
            new_cmd,
            input_dir,
            output_dir,
            args.old_cmd_args.clone(),
            args.new_cmd_args.clone(),
        )
    };

    config.validate()?;
    Ok(config)
}

#[tokio::main]
async fn main() -> Result<()> {
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

    if args.concurrent {
        reggr::execute_concurrent(&config).await?;
    } else {
        reggr::execute_sequential(&config)?;
    }

    Ok(())
}
