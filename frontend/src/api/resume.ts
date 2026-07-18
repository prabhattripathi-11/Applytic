import { api } from "./client";

export async function uploadResume(
    file: File,
    jobDescription: string
) {
    const formData = new FormData();

    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    const response = await api.post(
        "/resume/parse",
        formData
    );

    return response.data;
}