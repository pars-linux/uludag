class Student < ActiveRecord::Base
  has_many :comments
  has_many :documents

  accepts_nested_attributes_for :documents, :allow_destroy => true

  validates_uniqueness_of :name

  def score
    self.comments.inject(0) { |result, c| result + c.score }
  end

  def commented_by(user)
    self.comments.exists?(:commented_by => user.name)
  end
end
