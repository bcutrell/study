use criterion::{criterion_group, criterion_main, Criterion};
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};
use reggr::Config;
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;
use tempfile::tempdir;
use tokio::runtime::Runtime;

fn generate_test_files(test_dir: &PathBuf, num_files: usize) -> Vec<PathBuf> {
    fs::create_dir_all(test_dir).unwrap();
    let mut files = Vec::new();
    let mut rng = StdRng::seed_from_u64(42);
    for i in 0..num_files {
        let sleep_time = rng.gen_range(1.0..5.0);
        let content = format!("sleep_time={:.2}", sleep_time);
        let path = test_dir.join(format!("req_{:03}", i));
        let mut file = File::create(&path).unwrap();
        file.write_all(content.as_bytes()).unwrap();
        files.push(path);
    }
    files
}

fn create_test_script(dir: &PathBuf) -> PathBuf {
    let script_content = r#"#!/bin/bash
input_file=""
output_file=""

while [[ $# -gt 0 ]]; do
  case $1 in
    -i|--input)
      input_file="$2"
      shift 2
      ;;
    -o|--output)
      output_file="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$input_file" ]] || [[ -z "$output_file" ]]; then
  echo "Both input and output files must be specified"
  exit 1
fi

sleep_time=$(grep -o 'sleep_time=[0-9.]*' "$input_file" | cut -d= -f2)
sleep "$sleep_time"
echo "Completed after ${sleep_time}s" > "$output_file"
"#;
    let script_path = dir.join("test_script.sh");
    let mut file = File::create(&script_path).unwrap();
    file.write_all(script_content.as_bytes()).unwrap();
    Command::new("chmod")
        .arg("+x")
        .arg(&script_path)
        .status()
        .unwrap();
    script_path
}

fn execute_sequential(c: &mut Criterion) {
    let temp_dir = tempdir().unwrap();
    let test_dir = temp_dir.path().to_path_buf();
    let test_files = generate_test_files(&test_dir, 10);
    let script_path = create_test_script(&test_dir);
    let output_dir = test_dir.join("outputs");
    fs::create_dir_all(&output_dir).unwrap();

    c.bench_function("execute_sequential", |b| {
        b.iter(|| {
            for input in &test_files {
                let output = output_dir
                    .join(input.file_name().unwrap())
                    .with_extension("out");
                Command::new(&script_path)
                    .arg("-i")
                    .arg(input)
                    .arg("-o")
                    .arg(&output)
                    .status()
                    .unwrap();
            }
        })
    });
}

fn execute_concurrent(c: &mut Criterion) {
    let temp_dir = tempdir().unwrap();
    let test_dir = temp_dir.path().to_path_buf();
    generate_test_files(&test_dir, 10);
    let script_path = create_test_script(&test_dir);
    let output_dir = test_dir.join("outputs");
    fs::create_dir_all(&output_dir).unwrap();

    let rt = Runtime::new().unwrap();

    c.bench_function("execute_concurrent", |b| {
        b.iter(|| {
            let config = Config {
                preprocess: None,
                old_cmd: script_path.to_str().unwrap().to_string(),
                old_cmd_args: Some("-i {input} -o {output}".to_string()),
                new_cmd: script_path.to_str().unwrap().to_string(),
                new_cmd_args: Some("-i {input} -o {output}".to_string()),
                input_dir: test_dir.clone(),
                output_dir: output_dir.clone(),
                postprocess: None,
                concurrent: true,
            };

            rt.block_on(async {
                reggr::execute_concurrent(&config).await.unwrap();
            });
        })
    });
}

criterion_group! {
    name = benches;
    config = Criterion::default()
        .sample_size(10)
        .measurement_time(std::time::Duration::from_secs(20))
        .warm_up_time(std::time::Duration::from_secs(5));
    targets = execute_sequential, execute_concurrent
}
criterion_main!(benches);
