module OS
  def OS.windows?
    (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
  end
end

Vagrant.configure(2) do |config|
  config.vm.box = 'larryli/vivid64'
  config.vm.box_version = '20150325'

  config.vm.network 'forwarded_port', guest:5000, host:5000 # Exposed for development

  if OS.windows?()
    config.vm.synced_folder '.', '/vagrant', disabled: true
    config.vm.provider "virtualbox" do |vbox|
      vbox.gui = true
    end
  end
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
