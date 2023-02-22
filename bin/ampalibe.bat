@ echo off

IF /I "%1" == "env" (
    python -m ampalibe env
    exit /B
)

IF /I "%1" == "lang" (
    python -m ampalibe lang
    exit /B
)

IF /I "%1" == "create" (
    IF exist "%2" (
        echo ERROR !! %2 already exists  1>&2
        exit /B
    )
    python -m ampalibe create %2
    exit /B
)
IF /I "%1" == "init" (
    python -m ampalibe init
    exit /B
)
IF /I "%1" == "run" (

    IF NOT exist "core.py" (
        echo ERROR !! core.py not found  1>&2
        echo Please, go to your dir project.
        exit /B
    )

    IF NOT exist "conf.py" (
        echo ERROR !! conf.py not found  1>&2
        exit /B
    )

    call .env.bat
    python -m ampalibe run
    IF /I "%2" == "--dev" (
        watchmedo auto-restart --patterns="*.py;langs.json" --recursive -- python -c "import core;core.ampalibe.init.run()"
        exit /B
    )
    python -c "import core;core.ampalibe.init.run()"
    exit /B
)

IF /I "%1" == "version" (
    python -m ampalibe version
    exit /B
)

python -m ampalibe usage