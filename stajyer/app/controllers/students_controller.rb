class StudentsController < ApplicationController
  before_filter :login_required

  def index
    if params[:order].nil? or params[:order] == "score"
      @students = Student.all.sort {|a,b| b.score <=> a.score}
    else
      @students = Student.find(:all, :order => params[:order])
    end
  end

  def show
    @student = Student.find(params[:id])
    @comment = Comment.new(:student => @student)
  end

  def new
    @student = Student.new
    5.times { @student.documents.build }
  end

  def create
    @student = Student.new(params[:student])
    if @student.save
      flash[:notice] = 'Added successfully.'
      redirect_to students_url
    else
      render :action => :new
    end
  end

  def edit
    @student = Student.find(params[:id])
  end

  def update
    @student = Student.find(params[:id])
    if @student.update_attributes(params[:student])
      flash[:notice] = 'Updated succesfully.'
      redirect_to students_path
    else
      render :action => :edit
    end
  end

  def destroy
    @student = Student.find(params[:id])
    @student.destroy
    redirect_to students_url
  end
end
