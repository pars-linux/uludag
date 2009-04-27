# Be sure to restart your server when you modify this file.

# Your secret key for verifying cookie session data integrity.
# If you change this key, all old sessions will become invalid!
# Make sure the secret is at least 30 characters and all random, 
# no regular words or you'll be exposed to dictionary attacks.
ActionController::Base.session = {
  :key         => '_stajyer_session',
  :secret      => 'ed94bd7936833370dae20d62fe3d55d3f06627ead1a7d50c484bec39e2320387b6b4050b31eb4f07b142ecb93146e90458d6ed82b70e9f1fcde0250b5e22efe3'
}

# Use the database for sessions instead of the cookie-based default,
# which shouldn't be used to store highly confidential information
# (create the session table with "rake db:sessions:create")
# ActionController::Base.session_store = :active_record_store
