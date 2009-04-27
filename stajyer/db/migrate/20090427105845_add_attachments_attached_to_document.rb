class AddAttachmentsAttachedToDocument < ActiveRecord::Migration
  def self.up
    add_column :documents, :attached_file_name, :string
    add_column :documents, :attached_content_type, :string
    add_column :documents, :attached_file_size, :integer
    add_column :documents, :attached_updated_at, :datetime
  end

  def self.down
    remove_column :documents, :attached_file_name
    remove_column :documents, :attached_content_type
    remove_column :documents, :attached_file_size
    remove_column :documents, :attached_updated_at
  end
end
