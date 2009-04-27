class CreateStudents < ActiveRecord::Migration
  def self.up
    create_table :students do |t|
      t.string  :name
      t.string  :university
      t.string  :major
      t.integer :year
      t.text    :cover

      t.timestamps
    end
  end

  def self.down
    drop_table :students
  end
end
