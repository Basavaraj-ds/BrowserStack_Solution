from pydantic import BaseModel

class ArticleObject(BaseModel):
    title : str
    body : str = " "
    eng_title : str = ""


# # sample data
# sample_data = []
#
# sample_data.append(article(title="El rey está de vacaciones hoy", body=""))
# sample_data.append(article(title="el rey está con la reina", body=""))
# sample_data.append(article(title="el rey fue al palacio", body=""))
#
#
