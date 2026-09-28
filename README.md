# GitHub Pull Request ETL & Developer Behavior Analytics

## Overview

An end-to-end ETL pipeline that extracts Pull Request data from the **Microsoft VS Code GitHub repository**, transforms the API response into an analytical data model, and loads the resulting dataset into PostgreSQL.

The project is designed to support **developer behavior and contribution analytics**, including contribution frequency, contributor activity, Pull Request lifecycle, merge behavior, and temporal contribution patterns.

## Dataset

* **Source:** GitHub REST API
* **Repository:** `microsoft/vscode`
* **Entity:** Pull Request
* **Records:** 67,279 Pull Requests
* **Attributes:** 23
* **Grain:** One record per Pull Request

### Data Attributes

| Attribute          | Type        | Purpose                               |
| ------------------ | ----------- | ------------------------------------- |
| `pr_unique_id`     | BIGINT      | Unique GitHub Pull Request identifier |
| `pr_number`        | INTEGER     | Repository-specific PR number         |
| `author_id`        | BIGINT      | Unique contributor identifier         |
| `contributor_type` | TEXT        | GitHub contributor association        |
| `title`            | TEXT        | Pull Request title                    |
| `state`            | TEXT        | Current PR state                      |
| `draft`            | BOOLEAN     | Draft Pull Request indicator          |
| `created_at`       | TIMESTAMPTZ | PR creation timestamp                 |
| `updated_at`       | TIMESTAMPTZ | Last update timestamp                 |
| `closed_at`        | TIMESTAMPTZ | PR closure timestamp                  |
| `merged_at`        | TIMESTAMPTZ | PR merge timestamp                    |
| `created_year`     | INTEGER     | PR creation year                      |
| `created_month`    | INTEGER     | PR creation month                     |
| `created_hour`     | INTEGER     | PR creation hour                      |
| `updated_year`     | INTEGER     | Last update year                      |
| `updated_month`    | INTEGER     | Last update month                     |
| `updated_hour`     | INTEGER     | Last update hour                      |
| `closed_year`      | INTEGER     | Closure year                          |
| `closed_month`     | INTEGER     | Closure month                         |
| `closed_hour`      | INTEGER     | Closure hour                          |
| `merged_year`      | INTEGER     | Merge year                            |
| `merged_month`     | INTEGER     | Merge month                           |
| `merged_hour`      | INTEGER     | Merge hour                            |

## ETL Architecture

```text
GitHub REST API
      │
      ▼
   Extract
      │
      │  Pagination
      ▼
Raw Pull Request Records
      │
      ▼
  Transform
      │
      ├── Field selection
      ├── Identifier standardization
      ├── Datetime conversion
      ├── Null handling
      └── Time-derived attributes
      │
      ▼
Pandas DataFrame
      │
      ▼
    Load
      │
      ├── SQLAlchemy
      └── psycopg2
      │
      ▼
PostgreSQL
      │
      ▼
pull_requests_data
```

## Extraction

Pull Request records are retrieved through the GitHub REST API using authenticated requests and pagination.

The extraction process handles multiple API pages and consolidates the returned JSON records into a single dataset for transformation.

## Transformation

The transformation layer converts the nested GitHub API response into a structured relational dataset.

Key transformations include:

* Selecting analytical fields from the API response
* Standardizing identifiers
* Converting GitHub timestamps to timezone-aware datetime values
* Preserving nullable lifecycle timestamps such as `closed_at` and `merged_at`
* Deriving year, month, and hour attributes for temporal analysis
* Removing fields that are not required for the analytical model

## Loading

The transformed dataset is loaded into PostgreSQL using SQLAlchemy and psycopg2.

**Database:** `db_github_pr`
**Table:** `pull_requests_data`

The table is structured to support SQL-based analytical queries and downstream BI development.

## Developer Behavior Analytics

The dataset provides a foundation for analyzing developer contribution behavior across several dimensions.

### Contribution Activity

* Pull Requests per contributor
* Unique active contributors over time
* PR volume by month and year
* Contribution frequency

### Pull Request Lifecycle

Using the lifecycle timestamps:

```text
Created → Updated → Closed / Merged
```

the pipeline supports metrics such as:

* Time to merge
* Time to close
* PR age
* Lifecycle duration by contributor type

### Contribution Patterns

Temporal attributes enable analysis of:

* Monthly contribution trends
* Contributor activity over time
* Creation activity by hour
* Recurring versus occasional contribution patterns

### Contributor Segmentation

`author_id` and `contributor_type` enable contributor-level and contributor-segment analysis without relying on display names as identifiers.

## Analytical Questions

The resulting dataset can support questions such as:

* How does Pull Request activity change over time?
* How frequently do contributors submit Pull Requests?
* How many unique contributors are active during each period?
* What is the distribution of PR lifecycle duration?
* How does merge behavior vary across contributor types?
* Which periods have the highest contribution activity?
* How does individual contributor activity evolve over time?

## Technology Stack

* **Python**
* **Pandas**
* **Requests**
* **GitHub REST API**
* **SQLAlchemy**
* **psycopg2**
* **PostgreSQL**
* **pgAdmin**
* **VS Code**

## Project Outcome

The pipeline converts **67,279 GitHub Pull Request records into a structured PostgreSQL analytical dataset**, establishing a reusable foundation for developer behavior analysis, SQL analytics, and downstream dashboard development.
