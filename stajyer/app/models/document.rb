class Document < ActiveRecord::Base
  belongs_to :student
  has_attached_file :attached, :url => "/student/documents/:id/:style/:basename.:extension",
                               :path => ':rails_root/public/student/documents/:id/:style/:basename.:extension'
end
