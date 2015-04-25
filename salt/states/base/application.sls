application-packages:
  pkg.installed:
    - pkgs:
      - python: 2.7.9-1
      - python-dev: 2.7.9-1
      - virtualenv: 1.11.6+ds-1
    - install_recommends: False
    - reload_modules: True

/vagrant/venv:
  virtualenv.managed:
    - cwd: /vagrant
    - system_site_packages: False
    - requirements: /vagrant/requirements.txt
    - require:
        - pkg: application-packages
