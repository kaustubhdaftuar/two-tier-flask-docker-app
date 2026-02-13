#  Two-Tier Flask Application with CI/CD on AWS (Docker + Jenkins)

A production-style two-tier Flask application deployed on AWS EC2 using Docker and automated end-to-end with a Jenkins CI/CD pipeline triggered by GitHub webhooks.

---

##  Project Overview

This project demonstrates:

- Containerized Flask application
- MySQL database container
- Docker Compose orchestration
- Jenkins running inside Docker
- GitHub webhook-triggered CI/CD
- Automated Docker image rebuild and redeployment
- Deployment on AWS EC2 (Ubuntu)

The pipeline automatically rebuilds and redeploys the application on every push to the `main` branch.

---

##  Architecture Diagram

```
                        ┌──────────────────────────┐
                        │        Developer         │
                        │     (Push to GitHub)     │
                        └─────────────┬────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │        GitHub Repo       │
                        │   (Source Code Storage)  │
                        └─────────────┬────────────┘
                                      │  Webhook Trigger
                                      ▼
                  ┌────────────────────────────────────────┐
                  │        Jenkins (Docker Container)      │
                  │  - Runs Pipeline                       │
                  │  - Uses Docker Agent                   │
                  │  - Talks to Docker via socket          │
                  └─────────────┬──────────────────────────┘
                                │
                                ▼
                  ┌────────────────────────────────────────┐
                  │        Docker Engine (Host EC2)        │
                  │                                        │
                  │  docker compose down                   │
                  │  docker compose up -d --build          │
                  └─────────────┬──────────────────────────┘
                                │
                ┌───────────────┴────────────────┐
                ▼                                ▼
        ┌──────────────────┐            ┌──────────────────┐
        │ Flask App        │            │ MySQL Database   │
        │ Container        │            │ Container        │
        │ Port: 5001       │            │ Port: 3306       │
        └──────────────────┘            └──────────────────┘

                      Hosted on AWS EC2 (Ubuntu)
```

---

##  Tech Stack

- Python 3.10 (Flask)
- MySQL 8
- Docker
- Docker Compose (v2)
- Jenkins (Dockerized)
- GitHub Webhooks
- AWS EC2 (Ubuntu 22.04)

---

##  Project Structure

```
two-tier-flask-docker-app/
│
├── app/
│   ├── app.py
│   └── templates/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

##  Docker Setup

### Build & Run Manually

```bash
docker compose up -d --build
```

Access application:

```
http://<EC2_PUBLIC_IP>:5001
```

---

##  CI/CD Pipeline (Jenkins)

The Jenkins pipeline performs:

1. Clone repository from GitHub
2. Stop existing containers
3. Rebuild Docker image
4. Restart containers using Docker Compose

### Pipeline Script

```groovy
pipeline {
    agent {
        docker {
            image 'docker:27.0.3'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/kaustubhdaftuar/two-tier-flask-docker-app.git'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker compose down || true
                docker compose up -d --build
                '''
            }
        }
    }
}
```

---

##  Webhook Configuration

GitHub → Settings → Webhooks

**Payload URL:**

```
http://<EC2_PUBLIC_IP>:8080/github-webhook/
```

Content Type:

```
application/json
```

Trigger:

```
Just the push event
```

Now every push to `main` automatically triggers deployment.

---

##  Infrastructure Configuration

### EC2 Configuration

- Instance Type: t3.micro (Free Tier)
- Ubuntu 22.04
- 20GB EBS Volume
- 1GB Swap configured
- Ports Open:
  - 22 (SSH)
  - 5001 (Flask App)
  - 8080 (Jenkins)

---

##  Production Considerations

For real-world deployment:

- Remove `container_name` from compose file
- Use reverse proxy (Nginx)
- Add HTTPS with Let's Encrypt
- Use separate CI and App instances
- Store secrets securely (not in repo)
- Use managed CI like GitHub Actions for scale

---

##  What This Project Demonstrates

- Infrastructure debugging (disk resize, swap tuning)
- Container orchestration with Docker Compose
- Jenkins inside Docker controlling host Docker
- GitHub webhook automation
- End-to-end CI/CD pipeline
- Cloud deployment on AWS

---

##  Example Flow

```
Edit code → git push → Jenkins auto-build →
Docker rebuild → Containers restart → App updated live
```

No manual intervention required.

---

##  Learning Outcomes

This project covers real-world DevOps concepts:

- Immutable containers
- CI/CD automation
- Webhook-based triggers
- Docker socket mounting
- Resource optimization on low-memory instances
- Infrastructure troubleshooting

---

