# Vignesh Nambiar - Portfolio

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://notvikke.github.io/portfolio/)
[![Hugo](https://img.shields.io/badge/Built%20with-Hugo-ff4088)](https://gohugo.io/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)

## 🚀 About

Professional portfolio website showcasing my work as an **AI Engineer & Full-Stack Developer**. Built with Hugo and the Hugo Blox framework, featuring automated GitHub statistics, project showcases, and professional experience.

**Live Site**: [https://notvikke.github.io/portfolio/](https://notvikke.github.io/portfolio/)

## ✨ Features

- 📊 **Automated GitHub Stats Dashboard** - Real-time metrics updated weekly via GitHub Actions
- 🎨 **Modern, Responsive Design** - Clean emerald theme with dark mode support
- 📱 **Mobile-First** - Optimized for all devices
- 🚀 **Fast & Lightweight** - Static site generation with Hugo
- 📈 **Project Showcase** - 11+ featured projects with live demos and GitHub links
- 📄 **Downloadable Resume** - Always up-to-date CV in PDF format

## 🛠️ Tech Stack

- **Framework**: [Hugo](https://gohugo.io/) (Static Site Generator)
- **Theme**: [Hugo Blox](https://hugoblox.com/) (formerly Wowchemy)
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Analytics**: GitHub Stats API (GraphQL)

## 📊 GitHub Stats Dashboard

The portfolio features an automated "Open Source Impact" dashboard that displays:
- Total Repositories
- Lines of Code
- Active Projects (Last 90 Days)
- Contributions (Last 12 Months)

Stats are automatically updated weekly via GitHub Actions workflow.

## 🚀 Quick Start

### Prerequisites
- [Hugo Extended](https://gohugo.io/installation/) (v0.112.0 or later)
- [Go](https://go.dev/dl/) (v1.19 or later)

### Local Development

```bash
# Clone the repository
git clone https://github.com/notvikke/portfolio.git
cd portfolio

# Install dependencies
hugo mod get -u

# Start development server
hugo server -D

# Build for production
hugo --minify
```

Visit `http://localhost:1313` to view the site locally.

## 📁 Project Structure

```
portfolio/
├── .github/workflows/    # GitHub Actions (stats updater, deployment)
├── assets/              # Custom CSS/JS
├── content/             # Markdown content
│   ├── authors/admin/   # Profile information
│   ├── project/         # Project showcases
│   └── publication/     # Publications (if any)
├── data/                # GitHub stats JSON
├── layouts/             # Custom Hugo layouts
│   └── partials/        # Footer with stats dashboard
├── scripts/             # Python scripts (GitHub stats fetcher)
├── static/uploads/      # Resume PDF and media files
└── config/_default/     # Hugo configuration
```

## 🔧 Configuration

Key configuration files:
- `config/_default/params.yaml` - Site parameters, theme settings
- `config/_default/config.yaml` - Base Hugo configuration
- `content/authors/admin/_index.md` - Profile and bio information

## 📝 Updating Content

### Profile Information
Edit `content/authors/admin/_index.md` to update:
- Bio and professional summary
- Work experience
- Education
- Skills
- Certifications

### Projects
Add new projects in `content/project/[project-name]/index.md`:
```yaml
---
title: Project Name
date: 2026-01-19
external_link: https://github.com/username/repo
tags:
  - Tag1
  - Tag2
---
Project description here.
```

### Resume
Replace `static/uploads/resume.pdf` with your updated CV.

## 🤖 GitHub Actions Workflows

### Update GitHub Stats
- **Schedule**: Weekly (Sundays at midnight UTC)
- **Script**: `scripts/update_github_stats.py`
- **Output**: `data/github_stats.json`

### Deploy to GitHub Pages
- **Trigger**: Push to `main` branch
- **Action**: Builds and deploys Hugo site

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Built with [Hugo](https://gohugo.io/)
- Theme by [Hugo Blox](https://hugoblox.com/)
- Icons from [Lucide](https://lucide.dev/)

## 📧 Contact

**Vignesh Nambiar**
- Email: 97vigneshvn@gmail.com
- LinkedIn: [linkedin.com/in/97vigneshvn](https://linkedin.com/in/97vigneshvn)
- GitHub: [github.com/notvikke](https://github.com/notvikke)
- Portfolio: [notvikke.github.io/portfolio](https://notvikke.github.io/portfolio/)

---

⭐ **Star this repo** if you found it helpful!
