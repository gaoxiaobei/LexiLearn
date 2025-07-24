# LexiLearn Release Checklist

This checklist ensures all necessary steps are completed for a successful release of LexiLearn.

## Pre-Release Preparation

### Code Quality Checks
- [ ] All unit tests pass (`python -m pytest tests/unit`)
- [ ] All integration tests pass (`python -m pytest tests/integration`)
- [ ] All end-to-end tests pass (`python -m pytest tests/e2e`)
- [ ] Code coverage is above 90% (`python -m pytest --cov=lexilearn`)
- [ ] Code formatting is correct (`black .`)
- [ ] Code passes linting (`flake8 .`)
- [ ] Type checking passes (`mypy .`)
- [ ] Security scan passes (`bandit -r lexilearn`)
- [ ] No critical issues in dependency scan (`safety check`)

### Documentation Updates
- [ ] README.md is up to date
- [ ] CHANGES.md is updated with release notes
- [ ] All API documentation is current
- [ ] Installation guide is accurate
- [ ] Usage examples are working

### Versioning
- [ ] Version number is updated in `pyproject.toml`
- [ ] Version number is updated in `setup.cfg`
- [ ] Version number is consistent across all files
- [ ] Version bump is committed to git

## Build Process

### Package Build
- [ ] Clean previous builds (`rm -rf dist/ build/ *.egg-info`)
- [ ] Build source distribution (`python -m build --sdist`)
- [ ] Build wheel distribution (`python -m build --wheel`)
- [ ] Verify build contents (`tar -tzf dist/lexilearn-*.tar.gz`)
- [ ] Check package metadata (`python -m twine check dist/*`)

### Local Installation Test
- [ ] Create fresh virtual environment
- [ ] Install package from local build (`pip install dist/lexilearn-*.whl`)
- [ ] Test console scripts (`lexilearn --help`, `lexilearn-setup`, `lexilearn-validate`)
- [ ] Verify all dependencies are correctly installed
- [ ] Test basic functionality with sample data

## Testing

### Functionality Testing
- [ ] Test article processing with sample text
- [ ] Test vocabulary management features
- [ ] Test translation functionality (requires API key)
- [ ] Test configuration options
- [ ] Test error handling scenarios
- [ ] Test logging functionality

### Cross-Platform Testing
- [ ] Test on Linux
- [ ] Test on Windows
- [ ] Test on macOS
- [ ] Test with different Python versions (3.8, 3.9, 3.10, 3.11, 3.12)

### Performance Testing
- [ ] Test with small article (< 100 words)
- [ ] Test with medium article (100-1000 words)
- [ ] Test with large article (> 1000 words)
- [ ] Verify memory usage is reasonable
- [ ] Verify processing time is acceptable

## Publication

### PyPI Release
- [ ] Create release tag in git (`git tag -a v1.0.0 -m "Release version 1.0.0"`)
- [ ] Push tag to repository (`git push origin v1.0.0`)
- [ ] Upload to Test PyPI first (`python -m twine upload --repository testpypi dist/*`)
- [ ] Verify Test PyPI release works correctly
- [ ] Upload to PyPI (`python -m twine upload dist/*`)
- [ ] Verify PyPI release page shows correct information

### GitHub Release
- [ ] Create GitHub release from tag
- [ ] Add release notes to GitHub release
- [ ] Attach distribution files to GitHub release
- [ ] Publish GitHub release

## Post-Release Verification

### Installation Verification
- [ ] Test installation from PyPI (`pip install lexilearn`)
- [ ] Test installation in clean environment
- [ ] Verify all console scripts work
- [ ] Test basic functionality

### Documentation Verification
- [ ] Verify README.md renders correctly on PyPI
- [ ] Verify documentation links work
- [ ] Verify API documentation is accessible

### Communication
- [ ] Announce release on relevant channels
- [ ] Update project website if applicable
- [ ] Notify maintainers of dependent projects

## Rollback Plan

### If Issues Are Discovered
- [ ] Immediately assess severity of issue
- [ ] If critical, yank release from PyPI (`python -m twine remove dist/lexilearn-1.0.0*`)
- [ ] Create issue tracking the problem
- [ ] Develop fix in separate branch
- [ ] Plan hotfix release

## Notes

- This checklist should be reviewed and updated for each release
- Some steps may be automated in CI/CD pipelines
- Always test in environments that match production as closely as possible
- Keep detailed records of any issues encountered during the release process