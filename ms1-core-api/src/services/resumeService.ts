import axios, { AxiosError } from "axios";

/**
 * Base URL of the MS2 Resume Matching Service.
 *
 * Change this to an environment variable later:
 * process.env.MS2_URL
 */
const MS2_BASE_URL = "http://ms2:8000";

/**
 * Request body sent to MS2.
 */
export interface ParseResumeRequest {
    resume_path: string;
    job_description: string;
}

/**
 * Response returned from MS2.
 * Keep it flexible for now.
 */
export interface ParseResumeResponse {
    match_score: number;
    matched_skills: string[];
    missing_skills: string[];
    recommendations: string[];
    parsed_resume: Record<string, any>;
    errors: string[];
}

/**
 * Calls the MS2 Resume Matching Agent.
 */
export async function parseResume(
    resume_path: string,
    job_description: string
): Promise<ParseResumeResponse> {
    try {
        const payload: ParseResumeRequest = {
            resume_path,
            job_description,
        };

        const response = await axios.post<ParseResumeResponse>(
            `${MS2_BASE_URL}/parse-resume`,
            payload,
            {
                headers: {
                    "Content-Type": "application/json",
                },
                timeout: 60000,
            }
        );

        return response.data;
    } catch (error) {
        const err = error as AxiosError;

        if (err.response) {
            throw new Error(
                `MS2 Error (${err.response.status}): ${JSON.stringify(
                    err.response.data
                )}`
            );
        }

        if (err.request) {
            throw new Error(
                "Unable to connect to MS2 Resume Matching Service."
            );
        }

        throw new Error(err.message);
    }
}