# coolify-zdd-testapp

A deliberately tiny HTTP app used to measure Coolify deployment downtime for the
LearnWithHasan guide on zero-downtime deployments. The `main` branch evolves through
the guide's steps (no health check -> Dockerfile HEALTHCHECK -> tuned start-period);
the `compose` branch deploys the same app as a Docker Compose resource.

Env knobs: `APP_VERSION` (shown in every response), `STARTUP_DELAY_S` (sleep before
binding the port, simulates slow boot), `GRACEFUL` ("1" = drain on SIGTERM).
