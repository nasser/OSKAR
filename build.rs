use std::process::Command;

fn git_short_hash() -> String {
    let output = Command::new("git").args(&["rev-parse", "--short", "HEAD"]).output().unwrap();
    String::from_utf8(output.stdout).unwrap()
}

fn git_branch() -> String {
    let output = Command::new("git").args(&["rev-parse", "--abbrev-ref", "HEAD"]).output().unwrap();
    String::from_utf8(output.stdout).unwrap()
}

fn date() -> String {
    let output = Command::new("date").output().unwrap();
    String::from_utf8(output.stdout).unwrap()
}

fn main() {
    println!("cargo:rustc-env=GIT_HASH={}", git_short_hash());
    println!("cargo:rustc-env=GIT_BRANCH={}", git_branch());
    println!("cargo:rustc-env=BUILD_DATE={}", date());
}