# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Quant Dashboard, please report it by:

1. **Do NOT** open a public issue
2. Send an email to the maintainers (update with your contact)
3. Include detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond to security reports within 48 hours and will work to resolve issues promptly.

## Security Best Practices

When using Quant Dashboard:

- Keep dependencies up to date
- Use environment variables for sensitive data (never commit credentials)
- Review `.gitignore` to ensure no sensitive files are committed
- Use HTTPS in production deployments
- Regularly update Python and system packages
