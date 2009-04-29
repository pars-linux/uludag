class ChangeCommentsReviewColumnType < ActiveRecord::Migration
  def self.up
    change_column :comments, :review, :text
  end

  def self.down
    change_column :comments, :review, :string
  end
end
