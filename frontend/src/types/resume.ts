export interface ResumeResponse {
    match_score: number;
    matched_skills: string[];
    missing_skills: string[];
    recommendations: string[];

    parsed_resume: {
        full_name: string;
        email: string;
        phone: string;
        summary: string;
        skills: string[];
    };

    errors: string[];
}