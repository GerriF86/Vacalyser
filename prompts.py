# prompts.py
from core_functions import get_index_for_value

def generate_job_ad_prompt(data, job_title):
    """Generates the prompt for creating the job advertisement."""
    prompt = f"""
Create a compelling and informative job ad for the position of {job_title} using the following information:
{data}
The job ad should be structured in the following way:
1. **Introduction:** A brief and engaging introduction about the company, its mission, and its culture.
2. **About the Role:** A concise description of the role and its key responsibilities. Use action verbs and highlight the impact of the role within the organization.
3. **Responsibilities:** A detailed list of the main tasks and duties associated with the position. Be specific and use bullet points for clarity.
4. **Required Skills and Qualifications:** A clear outline of the essential skills, experience, and qualifications needed for the role. Differentiate between required and desired qualifications.
5. **Benefits and Perks:** A section showcasing the benefits and perks of working for the company. Highlight unique offerings that set the company apart.
6. **Call to Action:** A compelling call to action that encourages candidates to apply and provides instructions on how to do so.
Please ensure the job ad is:
- **Attractive:** Use an appealing and engaging tone to attract top talent.
- **Informative:** Provide all necessary information for candidates to understand the role and the company.
- **Inclusive:** Use inclusive language and avoid any discriminatory statements.
- **SEO-friendly:** Incorporate relevant keywords to improve the ad's visibility in search engines. (e.g. use the job title and location multiple times)
- **Target Audience-Specific:** Tailor the language and tone to appeal to the specific target audience for the position.
- **Highlight the company culture**: Make sure to communicate the company's values, work environment, and overall culture throughout the ad, especially in the introduction and benefits sections.
- **Specific and detailed**: The more details you can provide the better.
- **Formatted clearly**: The job ad should be easy to read and navigate, use bold text, bullet points and line breaks to improve readability.
- **No longer than necessary**: Keep it concise.
"""
    return prompt

def generate_interview_questions_prompt(data, job_title):
    """Generates the prompt for creating interview questions."""
    prompt = f"""
Based on the provided information, generate a set of insightful and relevant interview questions for the position of {job_title}.
The questions should cover the following areas:
1. **General Questions:**
   -  Questions about the candidate's background, experience, and career goals.
   -  Motivation for applying for the position and interest in the company.
   -  Strengths and weaknesses, and how they relate to the role.
2. **Technical Skills and Qualifications:**
   -  Questions that assess the candidate's technical skills, knowledge, and experience relevant to the required and desired qualifications.
   -  Specific questions related to tools, technologies, and methodologies mentioned in the job description.
   - Use the following data: {data}
3. **Soft Skills and Personality Traits:**
   -  Questions that evaluate the candidate's soft skills, such as communication, teamwork, problem-solving, and leadership abilities.
   -  Inquiries about the candidate's work style, adaptability, and ability to handle challenges.
4. **Experience with Specific Tasks:**
   -  Questions that delve into the candidate's past experience with tasks and responsibilities similar to those outlined in the job description.
   -  Requests for specific examples of how the candidate has demonstrated relevant skills or handled relevant situations in the past.
5. **Company Culture and Values Fit:**
   -  Questions that assess the candidate's alignment with the company's culture, values, and work environment.
   -  Inquiries about the candidate's understanding of the company's mission and how they see themselves contributing to it.
6. **Behavioral Questions:**
   -  Questions that ask the candidate to describe past behavior in specific situations to predict future performance.
   -  Examples: "Tell me about a time you had to deal with a difficult coworker," or "Describe a situation where you had to overcome a significant challenge."
7. **Situational Questions:**
   -  Questions that present the candidate with hypothetical scenarios related to the job and ask how they would respond.
   -  Examples: "How would you handle a situation where you made a mistake that impacted a project deadline?" or "What would you do if you disagreed with your supervisor's decision?"
8. **Questions for the Interviewer:**
   -  Prompt the candidate to ask any questions they have about the role, the team, or the company.

Please ensure that the questions are:
- **Open-ended:** Encourage detailed and thoughtful responses.
- **Job-related:** Directly relevant to the requirements and responsibilities of the position.
- **Legal and Ethical:** Avoid any questions that could be considered discriminatory or invasive.
- **Varied:** Include a mix of different question types to get a comprehensive understanding of the candidate.
- **Prioritized:** Focus on the most critical areas for the role.
- **Clearly Formulated**:  Each question should be easy to understand and unambiguous.
- **Comprehensive**: The questions should cover all relevant aspects of the candidate's profile and suitability for the role.

The interview questions should provide a comprehensive evaluation of each candidate's suitability for the position of {job_title}.
"""
    return prompt

def generate_onboarding_checklist_prompt(data, job_title):
    """Generates the prompt for creating the onboarding checklist."""
    prompt = f"""
Based on the provided information, generate a detailed onboarding checklist for a new employee in the position of {job_title}.
The checklist should cover the following areas:
1. **Pre-First Day Preparations:**
   -  Tasks to be completed before the new employee's first day, such as setting up their workstation, creating accounts, and preparing necessary materials.
2. **First Day Activities:**
   -  A schedule for the new employee's first day, including introductions to team members, a tour of the office, and an overview of company policies.
3. **First Week Activities:**
   -  Tasks and activities to be completed during the first week, such as role-specific training, meetings with key stakeholders, and setting initial goals.
4. **First Month Activities:**
    -  Milestones to be reached during the first month, such as completing training modules, taking on specific responsibilities, and participating in team projects.
5. **Ongoing Support and Development:**
    -  Plans for continued support and professional development beyond the first month, such as regular check-ins, mentorship, and opportunities for further training.
{data}

The checklist should be:
- **Comprehensive:** Cover all essential aspects of the onboarding process.
- **Organized:** Presented in a clear and logical sequence, with specific tasks and timelines.
- **Customized:** Tailored to the specific roleand responsibilities of the position.
- **Helpful:** Provide resources, links, and contact information to assist the new employee.
- **Engaging:** Make the onboarding experience welcoming and positive for the new hire.
- **Measurable:** Include items that can be checked off as completed.

The onboarding checklist should ensure that the new employee has a smooth and successful start in their role as {job_title} and integrates well into the company.
"""
    return prompt

def generate_retention_strategies_prompt(data, job_title):
    """Generates the prompt for creating the employee retention strategies."""
    prompt = f"""
Considering the provided information and the specific requirements of the {job_title} position, develop a comprehensive set of employee retention strategies.
The strategies should address the following areas:
1. **Compensation and Benefits:**
   -  Propose competitive salary structures, bonuses, and financial incentives that align with industry standards and recognize employee contributions.
   -  Suggest non-monetary benefits such as health insurance, retirement plans, and paid time off that enhance overall job satisfaction.
2. **Work-Life Balance:**
   -  Recommend policies and practices that promote a healthy balance between work and personal life, such as flexible work arrangements, remote work options, and generous vacation policies.
   -  Suggest initiatives to reduce burnout and stress, such as wellness programs and mental health support.
3. **Career Development and Growth Opportunities:**
   -  Outline opportunities for professional development, including training programs, workshops, conferences, and certifications.
   -  Propose career advancement paths and internal promotion opportunities to encourage long-term commitment.
   -  Suggest mentorship programs and coaching initiatives to support employee growth.
4. **Recognition and Rewards:**
   -  Develop strategies for acknowledging and rewarding employee achievements, contributions, and milestones.
   -  Propose both formal and informal recognition programs, such as employee-of-the-month awards, peer-to-peer recognition, and public acknowledgment of accomplishments.
5. **Company Culture and Work Environment:**
   -  Recommend ways to foster a positive, inclusive, and supportive work environment that aligns with the company's values.
   -  Suggest initiatives to promote diversity, equity, and inclusion within the workplace.
   -  Propose strategies to enhance team cohesion, collaboration, and communication.
6. **Communication and Feedback:**
   -  Develop strategies for transparent and effective communication between management and employees.
   -  Suggest mechanisms for regular feedback, both from managers to employees and from employees to management.
   -  Propose initiatives to ensure that employee voices are heard and their concerns are addressed.
7. **Employee Engagement and Involvement:**
    -  Recommend ways to involve employees in decision-making processes and seek their input on company policies and initiatives.
    -  Suggest activities and events that promote employee engagement, such as team-building activities, social events, and volunteer opportunities.
{data}

Please ensure that the retention strategies are:
- **Tailored:** Specifically designed to address the needs and expectations of employees in the {job_title} role.
- **Realistic:** Feasible to implement within the company's resources and constraints.
- **Data-driven:** Based on relevant data and best practices in employee retention.
- **Holistic:** Address multiple aspects of the employee experience.
- **Long-term oriented:** Focus on sustainable strategies that promote long-term employee satisfaction and retention.

The employee retention strategies should help the company attract and retain top talent in the {job_title} position, ultimately contributing to a motivated, engaged, and productive workforce.
"""
    return prompt