class Comment < ActiveRecord::Base
  belongs_to :student

  SCORES = [['-4: Wow. This. Sucks.', -4],
            ['-3: Needs a lot of work', -3],
            ['-2: This is bad', -2],
            ['-1: I dont like this', -1],
            ['0: No score', 0],
            ['1: Might have potential', 1],
            ['2: Good', 2],
            ['3: Almost there', 3],
            ['4: Made. Of. Awesome.', 4]]
end
