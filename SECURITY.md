# Security Policy

## Reporting a Vulnerability

If you find a security issue, please do not publish exploit details in a public issue. Open a private report through GitHub security advisories if available, or contact the repository owner directly.

## Secret Handling

Never commit:

- API keys
- Access tokens
- Private certificates
- Personal user data
- Local environment files

Use environment variables or a local `.env` file that is excluded from Git.

## Voice Assistant Safety

Future automation features should require explicit approval before taking sensitive actions such as deleting files, sending messages, changing account settings, or making purchases.
