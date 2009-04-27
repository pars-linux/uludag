class CreateComments < ActiveRecord::Migration
  def self.up
    create_table :comments do |t|
      t.integer :student_id
      t.string :commented_by
      t.string :review
      t.integer :score

      t.timestamps
    end
  end

  def self.down
    drop_table :comments
  end
end
