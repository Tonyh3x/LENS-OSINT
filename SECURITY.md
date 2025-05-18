# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.4.x   | :white_check_mark: |
| < 1.4   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please contact us immediately via email at security@lens-osint.com.

Please include the following information:

- Your contact details
- A description of the vulnerability
- Steps to reproduce the vulnerability
- Any additional information that may be helpful

## Security Measures

### Application Security

1. **Input Validation**
   - All file uploads are validated
   - File size limit: 10MB
   - Maximum 5 files per request
   - Allowed file extensions: txt, doc, docx, pdf, png, jpg, jpeg, bmp

2. **Session Security**
   - Secure session cookies
   - Session timeout: 1 hour
   - CSRF protection
   - XSS protection

3. **Authentication**
   - No authentication required (public service)
   - Rate limiting: 50 requests per minute
   - IP blocking for suspicious activity

4. **Data Security**
   - File uploads are stored temporarily
   - Automatic cleanup of old files
   - Secure file handling
   - No sensitive data storage

### Infrastructure Security

1. **Web Server**
   - Nginx with TLS 1.2/1.3
   - HSTS enabled
   - Rate limiting
   - Security headers
   - Firewall rules

2. **Application Server**
   - Docker isolation
   - Resource limits
   - Regular updates
   - Monitoring

3. **Database**
   - SQLite with encryption
   - Regular backups
   - Access controls

### Monitoring & Logging

1. **Application Logs**
   - Detailed request logging
   - Error tracking
   - Security events
   - Performance metrics

2. **Security Alerts**
   - Automatic notifications
   - Regular security scans
   - Compliance checks

## Security Updates

We regularly update our dependencies and infrastructure to ensure the highest level of security. All security updates are documented in our CHANGELOG.md file.

## Security Testing

We perform regular security testing including:

- Code review
- Dependency scanning
- Security scanning
- Penetration testing
- Compliance checks
