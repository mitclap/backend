Vagrant.configure(2) do |config|
  config.vm.box = 'larryli/vivid64'

  config.vm.network 'forwarded_port', guest:5000, host:5000 # Exposed for development

  config.vm.synced_folder 'salt/states', '/srv/salt'

  config.vm.provision :salt do |salt|

    salt.install_master = false
    salt.install_type = 'stable'

    salt.minion_config = 'salt/minion'

    salt.run_highstate = true

    salt.verbose = true
    salt.colorize = true
  end
end
