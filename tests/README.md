# Tests Directory

This directory contains all test files and documentation for the Proposal Generator system.

## Test Files

### Automated Test Suite
- **automated_test_suite.py** - Main automated test suite with 15 comprehensive test cases
  - Run with: `python tests/automated_test_suite.py`
  - Tests all major scenarios: complete inputs, vague inputs, budget mismatches, timelines, tech stack, etc.
  - Outputs pass/fail results and summary statistics
  - Target: 90%+ pass rate

### Unit Tests

#### Calculator Tests
- **test_calculator.py** - Basic calculator functionality tests
- **test_new_calculator.py** - Enhanced calculator tests with context multipliers
- **test_enterprise_keywords.py** - Tests enterprise keyword detection and complexity scoring
- **test_before_after.py** - Before/after comparison of calculator enhancements

#### Sanity Check Tests
- **test_sanity_check.py** - Comprehensive sanity check functionality tests
- **test_amazon_fix.py** - Specific test for "Amazon-like platform for $5k" scenario
- **test_timeline.py** - Tests timeline warning detection (e.g., "e-commerce in 2 weeks")
- **test_ecommerce_timeline.py** - E-commerce specific timeline validation tests
- **test_sanity_integration.py** - Integration tests for sanity check in full workflow

#### Generation Tests
- **test_generation_with_warnings.py** - Tests proposal generation with warning sections

#### Other Tests
- **test_extraction.py** - Tests extraction node functionality
- **test_real_scenario.py** - Real-world scenario tests
- **test_summary.py** - Summary generation tests
- **version_test.py** - Version compatibility tests

## Documentation

### Feature Documentation
- **SANITY_CHECK_FEATURE.md** - Complete sanity check feature documentation
- **SANITY_CHECK_FIX.md** - Documentation of the Amazon $5k budget fix
- **SANITY_CHECK_QUICK_REF.md** - Quick reference guide for sanity check
- **SANITY_CHECK_SUMMARY.md** - Summary of sanity check capabilities
- **TIMELINE_FIX.md** - Documentation of timeline detection fix (e-commerce in 2 weeks)
- **automated_tests.MD** - Automated test suite changes and iteration log

## Test Logs
- **test_run_1.log** - First automated test run results (10/15 passed - 66.7%)
- **test_run_2.log** - Second test run (blocked by API quota)

## Running Tests

### Run All Automated Tests
```bash
python tests/automated_test_suite.py
```

### Run Individual Tests
```bash
# Calculator tests
python tests/test_calculator.py
python tests/test_new_calculator.py
python tests/test_enterprise_keywords.py

# Sanity check tests
python tests/test_sanity_check.py
python tests/test_amazon_fix.py
python tests/test_timeline.py

# Generation tests
python tests/test_generation_with_warnings.py
```

## Test Coverage

The test suite covers:
1. ✅ Complete detailed inputs with all fields
2. ✅ Vague inputs requiring clarification
3. ✅ Budget-scope mismatches (high and low)
4. ✅ Unrealistic timelines
5. ✅ Outdated technology detection
6. ✅ Enterprise complexity estimation
7. ✅ Compliance requirements (HIPAA, GDPR)
8. ✅ Multi-country/international projects
9. ✅ Migration projects
10. ✅ Empty/invalid inputs
11. ✅ Startup MVP scenarios
12. ✅ Enterprise integrations (SAP, Salesforce)
13. ✅ Duplicate deliverable handling

## Key Improvements Tested

### Calculator Enhancements
- MVP context detection (downgrades complexity for startup/basic projects)
- Enterprise keyword recognition (ERP, CRM, SAP, Oracle, etc.)
- Migration/legacy project handling
- Context-aware multipliers (Enterprise 1.3x, Compliance 1.2x, Migration 1.4x, International 1.2x)

### Sanity Check Enhancements
- Budget-scope mismatch detection
- Timeline reality checks (including pattern detection in user input)
- Platform comparison detection (Amazon, Facebook, Netflix, etc.)
- Outdated technology warnings (Flash, jQuery, etc.)
- Minimum budget thresholds

### Known Issues
- **API Quota Limitation**: Tests require OpenAI API access. If quota exceeded, tests will fail.
- **LLM Dependency**: No local fallback for extraction/validation/generation nodes.

## Test Results History

| Run | Date | Pass Rate | Notes |
|-----|------|-----------|-------|
| 1 | Oct 22 | 66.7% (10/15) | Initial run, identified 5 issues |
| 2 | Oct 22 | N/A | Blocked by API quota |

## Next Steps

1. Restore API quota or configure alternative LLM
2. Run automated_test_suite.py
3. Iterate on failures until 90%+ pass rate achieved
4. Add more edge case tests as needed
5. Consider implementing test mocking/caching for offline testing
