Binary building
===============

Here is an **experimental setup** for building a standalone binary of `galette` using Docker and PyInstaller. 


Purpose
=======

* Create a self-contained binary of the `galette` project without requiring Python on the target system.
* Use Docker to ensure a consistent build environment.


Usage
=====

1. Ensure Docker is installed and running.
2. Run the script:
   ```bash
   ./binary/compile-binary.sh
   ```

The finished binary can be found in `binary/dist/galette`.


Notes
=====

- **Experimental**: This setup is untested and may require adjustments to work correctly for your project and dependencies.
- **Requirements**: Ensure PyInstaller supports all dependencies in your project.


To do
=====

- Add testing and validation for compatibility across systems.
- Improve error handling for failures during the build process.
- Optimize the Docker image for smaller size and faster builds.
