class Config:

    class files:
        save_folder = 'save_files'
        articles_urls_list = f'{save_folder}/articles_urls_list.txt'
        save_resume = f'{save_folder}/articles_resume.txt'
        save_scrapping_failed = f'{save_folder}/not_scrapping.txt'

    class API_KEY:
        groq_api_key = "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"


    class instruction_system:
        instruction = """ 
            SPEAK ONLY IN FRENCH
            You are used to summarize articles that will be given to you.
            Everything given to you must be summarized without comment. You make the summary without other unnecessary comments.
            Here are instructions to be strictly followed:
            - Give answers directly without introductory sentences
            - You must take what the article is about, just what the article is about and nothing else
            - Be as simple as possible
            - First, you state precisely what the article is about, then you make a summary, afterwards you summarize the article in a few points and you take the points
        """