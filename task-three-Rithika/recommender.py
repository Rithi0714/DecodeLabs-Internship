

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



job_roles = {
    "Data Scientist": "python sql machine learning data analysis statistics pandas numpy scikit-learn",
    "Backend Developer": "python java sql apis rest databases django flask algorithms data structures",
    "Frontend Developer": "html css javascript react nodejs ui ux design responsive web",
    "DevOps Engineer": "aws docker kubernetes linux git ci cd cloud automation bash",
    "ML Engineer": "python machine learning deep learning tensorflow pytorch neural networks nlp",
    "Data Analyst": "sql excel python data visualization power bi tableau statistics reporting",
    "Cloud Architect": "aws azure cloud docker kubernetes infrastructure networking security devops",
    "Full Stack Developer": "html css javascript react python django sql rest apis git nodejs",
    "Cybersecurity Analyst": "networking security linux ethical hacking firewalls encryption python bash",
    "AI Engineer": "python machine learning deep learning nlp computer vision tensorflow algorithms"
}


role_names = list(job_roles.keys())
role_skills = list(job_roles.values())


def get_recommendations(user_skills_input, top_n=3):

    all_docs = [user_skills_input] + role_skills

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    top_indices = similarity_scores.argsort()[::-1][:top_n]

    results = []
    for i in top_indices:
        results.append({
            "role": role_names[i],
            "score": round(similarity_scores[i] * 100, 2),
            "required_skills": role_skills[i]
        })

    return results


def show_results(results, user_input):
    print(f"\nYour skills: {user_input}")
    print(f"\nTop {len(results)} matching job roles for you:\n")

    for rank, job in enumerate(results, start=1):
        print(f"  {rank}. {job['role']}")
        print(f"     Match Score : {job['score']}%")
        print(f"     Role needs  : {job['required_skills']}")
        print()


def main():
    print("Tech Stack Recommender")
    print("Enter your skills and I will suggest the best matching job roles.")
    print("Type 'quit' to exit.\n")

    while True:
        print("Enter at least 3 skills you know (example: python sql machine learning)")
        user_input = input("Your skills : ").strip().lower()

        if user_input == 'quit':
            print("Goodbye!")
            break

        if not user_input:
            print("Please enter something.\n")
            continue

        skills_entered = user_input.split()
        if len(skills_entered) < 3:
            print("Please enter at least 3 skills for better recommendations.\n")
            continue

     
        recommendations = get_recommendations(user_input, top_n=3)

        if recommendations[0]['score'] == 0:
            print("No strong match found. Try entering more specific tech skills.\n")
            continue

        show_results(recommendations, user_input)

        again = input("Want to try with different skills? (yes / quit) : ").strip().lower()
        if again != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()