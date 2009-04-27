class Student < ActiveRecord::Base
  has_many :comments
  has_many :documents

  accepts_nested_attributes_for :documents, :allow_destroy => true

  def score
    result = 0
    self.comments.each { |c| result += c.score }
    return result
  end
end
