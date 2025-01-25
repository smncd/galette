Binary building
===============

Here is an **experimental setup** for building a standalone binary of `galette` using Docker and PyInstaller. No testing has been done as to how this scales, works across systems, etc.


Purpose
-------

* Create a self-contained binary of the `galette` project without requiring Python on the target system.
* Use Docker to ensure a consistent build environment.


Usage
-----

1. Ensure Docker is installed and running.
2. Run the script:
   ```bash
   ./binary/compile-binary.sh
   ```

The finished binary can be found in `binary/dist/galette`.
