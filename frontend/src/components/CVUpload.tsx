// src/components/CVUpload.tsx
import React, { useState } from 'react';
import { uploadCV, analyzeSkills } from '../services/api';

const CVUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError(null);
        setResult(null);
      } else {
        setError('Please upload a PDF or DOCX file');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsLoading(true);
    setError(null);
    setUploadProgress(10);
    
    try {
      const uploadResponse = await uploadCV(file);
      setUploadProgress(50);
      
      const cvData = uploadResponse.data;
      const skills = cvData.skills || [];
      const experience = cvData.experience || 0;
      
      if (skills.length === 0) {
        throw new Error('No skills detected in your CV. Please try a different file.');
      }
      
      const analysisResponse = await analyzeSkills(skills, experience);
      setUploadProgress(100);
      
      setResult(analysisResponse.recommendations);
      
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.message || 'Upload failed. Please try again.');
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  const renderLearningPath = (path: any[]) => {
    if (!path || path.length === 0) return null;
    
    return path.map((item: any, idx: number) => {
      if (typeof item === 'string') {
        return (
          <div key={idx} className="flex items-start space-x-3 p-2 bg-white rounded-lg border border-indigo-100">
            <div className="flex-shrink-0 w-6 h-6 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold text-xs">
              {idx + 1}
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">{item}</p>
            </div>
          </div>
        );
      }
      
      return (
        <div key={idx} className="flex items-start space-x-3 p-2 bg-white rounded-lg border border-indigo-100">
          <div className="flex-shrink-0 w-6 h-6 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold text-xs">
            {idx + 1}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-900">
              {item.step || item}
              {item.priority === 'High' && (
                <span className="ml-2 text-xs text-red-500 font-bold">⚡ Priority</span>
              )}
            </p>
            {item.related_skills && item.related_skills.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-1">
                {item.related_skills.map((s: string, ri: number) => (
                  <span key={ri} className="text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded-full">
                    {s} 📚
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      );
    });
  };

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="bg-white rounded-xl shadow-md p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
            <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Upload Your CV
          </h1>
          <p className="text-gray-600">
            Get personalized career recommendations powered by AI
          </p>
          <div className="mt-2 inline-flex items-center space-x-2 text-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span className="text-gray-500">Connected to AI Backend</span>
          </div>
        </div>

        <div className={`border-2 border-dashed rounded-xl p-12 text-center transition-all
          ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 hover:border-blue-400'}`}>
          <input
            type="file"
            id="cv-upload"
            className="hidden"
            accept=".pdf,.docx"
            onChange={handleFileChange}
          />
          <label
            htmlFor="cv-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <svg className="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-lg font-medium text-gray-700">
              {file ? file.name : 'Click to select or drag and drop'}
            </p>
            <p className="text-sm text-gray-500 mt-2">
              PDF or DOCX files supported • Max size: 10MB
            </p>
          </label>
        </div>

        {uploadProgress > 0 && uploadProgress < 100 && (
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Processing your CV...</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 rounded-full h-2 transition-all duration-500"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || isLoading}
          className={`w-full mt-6 py-3 text-base rounded-lg font-medium transition-all
            ${!file || isLoading 
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
              : 'bg-blue-600 text-white hover:bg-blue-700'}`}
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing with AI...
            </span>
          ) : (
            'Upload & Analyze'
          )}
        </button>

        {/* RESULTS SECTION */}
        {result && (
          <div className="mt-6 space-y-4 animate-fade-in">
            {/* Header */}
            <div className="p-4 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg">
              <h3 className="font-semibold text-lg text-green-800">🎯 AI Analysis Complete!</h3>
              <p className="text-sm text-gray-600">Here are your personalized career recommendations</p>
            </div>
            
            {/* Career Cluster & Match */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm font-medium text-gray-700">Your Career Cluster</p>
                <p className="text-2xl font-bold text-blue-600">{result.cluster_name || 'N/A'}</p>
                <p className="text-sm text-gray-500 mt-1">
                  {result.career_info?.description || 'Career path based on your skills'}
                </p>
                {result.career_info?.industry && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {result.career_info.industry.slice(0, 3).map((ind: string, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-blue-200 text-blue-800 rounded-full">
                        {ind}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                <p className="text-sm font-medium text-gray-700">Match Score</p>
                <div className="flex items-center space-x-3">
                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-purple-600 rounded-full h-3 transition-all duration-1000"
                      style={{ width: `${result.match_percentage || 0}%` }}
                    />
                  </div>
                  <span className="font-bold text-xl">{result.match_percentage || 0}%</span>
                </div>
                <p className="text-sm text-gray-500 mt-1">{result.career_potential || 'Building your career'}</p>
                {result.time_estimate && (
                  <p className="text-sm text-gray-500">⏱️ {result.time_estimate}</p>
                )}
                {result.career_info?.salary_range && (
                  <p className="text-sm text-gray-500 mt-1">💰 {result.career_info.salary_range}</p>
                )}
              </div>
            </div>

            {/* Career Info Details */}
            {result.career_info && (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
                {result.career_info.growth_potential && (
                  <div>
                    <p className="text-xs text-gray-500">📈 Growth</p>
                    <p className="font-semibold text-sm">{result.career_info.growth_potential}</p>
                  </div>
                )}
                {result.career_info.remote_opportunities && (
                  <div>
                    <p className="text-xs text-gray-500">🏢 Remote</p>
                    <p className="font-semibold text-sm">{result.career_info.remote_opportunities}</p>
                  </div>
                )}
                {result.career_info.why_choose && (
                  <div className="col-span-2 md:col-span-1">
                    <p className="text-xs text-gray-500">💡 Why Choose This</p>
                    <p className="text-xs text-gray-700">{result.career_info.why_choose}</p>
                  </div>
                )}
              </div>
            )}

            {/* Project Idea */}
            {result.career_info?.project_idea && (
              <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <p className="text-sm font-medium text-gray-700">🚀 Project Idea</p>
                <p className="text-sm text-gray-700 mt-1">{result.career_info.project_idea}</p>
              </div>
            )}

            {/* Recommended Roles */}
            {result.recommended_roles && result.recommended_roles.length > 0 && (
              <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                <p className="text-sm font-medium text-gray-700">🎯 Recommended Roles</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.recommended_roles.map((role: string, idx: number) => (
                    <span key={idx} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                      {role}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Skill Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm font-medium text-gray-700">✅ Your Skills</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.skill_coverage?.has?.map((skill: string, idx: number) => (
                    <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              <div className="p-4 bg-red-50 rounded-lg border border-red-200">
                <p className="text-sm font-medium text-gray-700">📚 Skills to Develop</p>
                <div className="flex flex-wrap gap-2 mt-1">
                  {result.missing_skills?.map((skill: string, idx: number) => (
                    <span key={idx} className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs">
                      {skill}
                    </span>
                  ))}
                </div>
                <p className="text-sm text-gray-500 mt-1">{result.missing_skills?.length || 0} skills to learn</p>
              </div>
            </div>

            {/* Missing Skills with Resources */}
            {result.skill_resources?.missing_skills && 
             Object.keys(result.skill_resources.missing_skills).length > 0 && (
              <div className="p-4 bg-orange-50 rounded-lg border border-orange-200">
                <p className="text-sm font-medium text-gray-700 mb-3">📖 Learning Resources for Each Missing Skill</p>
                <div className="space-y-4">
                  {Object.entries(result.skill_resources.missing_skills).map(([skill, data]: [string, any]) => (
                    <div key={skill} className="bg-white p-4 rounded-lg border border-orange-100 shadow-sm">
                      <div className="flex items-center justify-between flex-wrap gap-2">
                        <h4 className="font-bold text-orange-800 text-lg">
                          {skill.charAt(0).toUpperCase() + skill.slice(1)}
                        </h4>
                        <div className="flex gap-2 flex-wrap">
                          {data.difficulty && (
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              data.difficulty === 'Beginner' ? 'bg-green-200 text-green-800' :
                              data.difficulty === 'Intermediate' ? 'bg-yellow-200 text-yellow-800' :
                              'bg-red-200 text-red-800'
                            }`}>
                              {data.difficulty}
                            </span>
                          )}
                          {data.learning_time && (
                            <span className="text-xs px-2 py-1 bg-gray-200 text-gray-700 rounded-full">
                              ⏱️ {data.learning_time}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      {data.description && (
                        <p className="text-sm text-gray-700 mt-2">{data.description}</p>
                      )}
                      
                      {data.why_learn && (
                        <div className="mt-2 p-2 bg-blue-50 rounded border border-blue-100">
                          <p className="text-xs text-blue-700 font-medium">💡 Why learn this?</p>
                          <p className="text-sm text-blue-800">{data.why_learn}</p>
                        </div>
                      )}
                      
                      {data.resources && data.resources.length > 0 && (
                        <div className="mt-3">
                          <p className="text-xs text-gray-500 font-medium mb-1">📚 Resources:</p>
                          <div className="flex flex-wrap gap-2">
                            {data.resources.map((res: any, ridx: number) => (
                              <a
                                key={ridx}
                                href={res.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center text-xs px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full hover:bg-blue-100 hover:text-blue-900 transition-colors border border-blue-200"
                              >
                                <span className="mr-1">🔗</span>
                                {res.name}
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {data.certification && (
                        <div className="mt-2 p-2 bg-green-50 rounded border border-green-100">
                          <p className="text-xs text-green-700 font-medium">🎓 Certification:</p>
                          <p className="text-sm text-green-800">{data.certification}</p>
                        </div>
                      )}
                      
                      {data.projects && data.projects.length > 0 && (
                        <div className="mt-2">
                          <p className="text-xs text-gray-500 font-medium">📁 Project Ideas:</p>
                          <ul className="list-disc list-inside text-sm text-gray-700 mt-1">
                            {data.projects.slice(0, 2).map((proj: string, pi: number) => (
                              <li key={pi}>{proj}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {data.job_demand && (
                        <p className="text-xs text-gray-500 mt-2">📊 {data.job_demand}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Learning Path */}
            {result.learning_path && result.learning_path.length > 0 && (
              <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                <p className="text-sm font-medium text-gray-700 mb-3">🗺️ Your Learning Roadmap</p>
                <div className="space-y-2">
                  {renderLearningPath(result.learning_path)}
                </div>
              </div>
            )}

            {/* Alternative Paths */}
            {result.alternative_paths && result.alternative_paths.length > 0 && (
              <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p className="text-sm font-medium text-gray-700 mb-3">🔄 Alternative Career Paths</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {result.alternative_paths.slice(0, 3).map((alt: any, idx: number) => (
                    <div key={idx} className="p-3 bg-white rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                      <p className="font-semibold text-sm text-gray-800">{alt.cluster_name}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                          <div 
                            className="bg-blue-600 rounded-full h-1.5"
                            style={{ width: `${alt.match_percentage || 0}%` }}
                          />
                        </div>
                        <span className="text-xs font-medium">{alt.match_percentage || 0}%</span>
                      </div>
                      {alt.missing_for_this && alt.missing_for_this.length > 0 && (
                        <div className="mt-1">
                          <p className="text-xs text-gray-500">Need: {alt.missing_for_this.join(', ')}</p>
                        </div>
                      )}
                      {alt.salary_range && (
                        <p className="text-xs text-gray-500 mt-1">💰 {alt.salary_range}</p>
                      )}
                      {alt.description && (
                        <p className="text-xs text-gray-500 mt-1">{alt.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => setResult(null)}
              className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors text-sm"
            >
              Upload Another CV
            </button>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div className="bg-white rounded-xl shadow-md p-4 text-center">
          <div className="inline-flex items-center justify-center w-10 h-10 bg-blue-100 rounded-full mb-2">
            <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="font-semibold text-sm">Real CV Parsing</h3>
          <p className="text-xs text-gray-500">Extract skills from your actual CV</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-4 text-center">
          <div className="inline-flex items-center justify-center w-10 h-10 bg-purple-100 rounded-full mb-2">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h3 className="font-semibold text-sm">ML Clustering</h3>
          <p className="text-xs text-gray-500">K-Means & DBSCAN algorithms</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-4 text-center">
          <div className="inline-flex items-center justify-center w-10 h-10 bg-green-100 rounded-full mb-2">
            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 className="font-semibold text-sm">Real-Time Analysis</h3>
          <p className="text-xs text-gray-500">Live AI-powered recommendations</p>
        </div>
      </div>
    </div>
  );
};

export default CVUpload;