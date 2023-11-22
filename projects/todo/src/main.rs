/*
 Learning about rust and htmx by following this great post:
 https://www.joeymckenzie.tech/blog/templates-with-rust-axum-htmx-askama

 pnpm dlx tailwindcss -i styles/tailwind.css -o assets/main.css --watch

  Run server:
  $ cargo watch -x run

  Run tailwind:
  $ pnpm dlx tailwindcss -i styles/tailwind.css -o assets/main.css --watch && cargo watch -x run
*/

// This is a part of the anyhow crate, which provides flexible error handling in Rust.
// The Context trait is used to add context to a Result type.
use anyhow::Context;

// askama is a type-safe, compiled Jinja-like template engine for Rust.
// The Template trait is used to define your own templates.
use askama::Template;

// axum is a web application framework for Rust.
// It provides various features like routing, request handling, and responses
use axum::{
    http::StatusCode,
    response::{Html, IntoResponse, Response},
    routing::get,
    Router,
};

// tower_http is a crate that provides additional utilities for HTTP services
use tower_http::services::ServeDir;

// tracing is a framework for instrumenting Rust programs to collect structured,
// event-based diagnostic information
use tracing::info;

use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use serde_json::json;


struct Todo {
    id: i32,
    description: String,
}

#[derive(Template)]
#[template(path = "todos.html")]
struct Records {
    todos: Vec<Todo>,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "todo=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    info!("initializing router...");
    let assets_path = std::env::current_dir().unwrap();
    let port = 8000_u16;
    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], port));

    // let api_router = Router::new().route("/todos", get(todos_from_the_server));

    let router = Router::new()
        .route("/", get(hello))
        .route("/todos", get(todos_from_the_server))
        .nest("/api", api_router)
        .nest_service(
            "/assets",
            ServeDir::new(format!("{}/assets", assets_path.to_str().unwrap())),
        );

    info!("router initialized, now listening on port {}", port);

    axum::Server::bind(&addr)
        .serve(router.into_make_service())
        .await
        .context("error while starting server")?;

    Ok(())
}

async fn todos_from_the_server() -> impl IntoResponse {
    let todo = vec![
        Todo {
            id: 1,
            description: "Buy milk".to_string(),
        },
        Todo {
            id: 2,
            description: "Buy eggs".to_string(),
        }
    ];

    Records { todos }
}

async fn hello() -> impl IntoResponse {
    let template = HelloTemplate {};
    HtmlTemplate(template)
}

#[derive(Template)]
#[template(path = "hello.html")]
struct HelloTemplate;

// A wrapper type that we'll use to encapsulate HTML
// parsed by askama into valid HTML for axum to serve.
struct HtmlTemplate<T>(T);

// Allows us to convert Askama HTML templates into valid HTML
// for axum to serve in the response.
impl<T> IntoResponse for HtmlTemplate<T>
where
    T: Template,
{
    fn into_response(self) -> Response {
        // Attempt to render the template with askama
        match self.0.render() {
            // If we're able to successfully parse and aggregate the template, serve it
            Ok(html) => Html(html).into_response(),
            // If we're not, return an error or some bit of fallback HTML
            Err(err) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                format!("Failed to render template. Error: {}", err),
            )
                .into_response(),
        }
    }
}
