class CommentsController < ApplicationController
  before_filter :login_required
  def create
    @student = Student.find(params[:student_id])
    @comment = @student.comments.build(params[:comment])
    @comment.commented_by = current_user.name
    @comment.save
    redirect_to student_url(@comment.student_id)
  end
end
