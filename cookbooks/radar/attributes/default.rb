# pgdg repo
override['postgresql']['enable_pgdg_yum'] = true

# postgresql 9.4
override['postgresql']['version'] = '9.4'
override['postgresql']['dir'] = '/var/lib/pgsql/9.4/data'
override['postgresql']['config']['data_directory'] = node['postgresql']['dir']
override['postgresql']['client']['packages'] = ['postgresql94', 'postgresql94-devel']
override['postgresql']['server']['packages'] = ['postgresql94-server']
override['postgresql']['server']['service_name'] = 'postgresql-9.4'
override['postgresql']['contrib']['packages'] = ['postgresql94-contrib']

# postgresql config
override['postgresql']['password']['postgres'] = 'vagrant'
override['postgresql']['config']['listen_addresses'] = '*'