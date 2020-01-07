### What is it?

It is a simple orm (pattern: active record), just for experience.


### Technology

Python 3.6


### Plan
| # | Task | Estimate | Progress |
| ------------ | ------------ | ------------ | ------------ |
| 1 | Design: orm(crud), prepare tables(sqlite, postgresql, mysql), tests. Select the tools and dependencies | 3h | DONE |
| 2 | Create project and prepare environment | 2h | DONE |
| 3 | Implement sql scripts for creating database and tables | 5h  | DONE |
| 4 | Implement active record pattern (create part) + tests | 8h  | DONE |
| 5 | Implement active record pattern (read part) + tests | 6h  | DONE |
| 6 | Implement active record pattern (update part) + tests | 7h  | DONE |
| 7 | Implement active record pattern (delete part) + tests | 5h  | DONE |
| 8 | Write documentation | 2h | DONE |


### Install

    git clone git@github.com:robin0371/myorm.git
    cd myorm
    activate env
    pip install -r requirements.txt
    docker-compose up

    # How it works? See tests


### Tests
    # Install docker and docker-compose

    # Run databases before tests:
    cd myorm
    docker-compose up

    # Run tests in another terminal:
    cd myorm
    activate env
    pytest --mypy --mypy-ignore-missing-imports --cov=myorm/
