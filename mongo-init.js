// MongoDB initialization script
db = db.getSiblingDB('interviewai');

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name", "role", "hashed_password", "is_active"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        role: {
          enum: ["student", "job_seeker", "admin"]
        },
        hashed_password: {
          bsonType: "string",
          minLength: 60,
          maxLength: 60
        },
        is_active: {
          bsonType: "bool"
        },
        created_at: {
          bsonType: "date"
        },
        updated_at: {
          bsonType: "date"
        }
      }
    }
  }
});

db.createCollection('resumes', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "file_name", "file_size", "content_type", "extracted_text", "is_processed"],
      properties: {
        user_id: {
          bsonType: "string"
        },
        file_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 255
        },
        file_size: {
          bsonType: "int",
          minimum: 0,
          maximum: 10485760  // 10MB
        },
        content_type: {
          bsonType: "string",
          enum: ["application/pdf"]
        },
        extracted_text: {
          bsonType: "string",
          minLength: 1
        },
        is_processed: {
          bsonType: "bool"
        },
        analysis: {
          bsonType: "object"
        },
        created_at: {
          bsonType: "date"
        },
        updated_at: {
          bsonType: "date"
        }
      }
    }
  }
});

db.createCollection('interview_sessions', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "job_role", "experience_level", "industry", "questions", "is_active", "is_completed"],
      properties: {
        user_id: {
          bsonType: "string"
        },
        job_role: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        experience_level: {
          enum: ["entry", "mid", "senior"]
        },
        industry: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        questions: {
          bsonType: "array",
          items: {
            bsonType: "object"
          }
        },
        answers: {
          bsonType: "array"
        },
        current_question_index: {
          bsonType: "int",
          minimum: 0
        },
        is_active: {
          bsonType: "bool"
        },
        is_completed: {
          bsonType: "bool"
        },
        started_at: {
          bsonType: "date"
        },
        completed_at: {
          bsonType: "date"
        }
      }
    }
  }
});

db.createCollection('feedback_reports', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["session_id", "user_id", "performance_metrics", "strength_areas", "improvement_areas", "detailed_feedback", "recommended_practice_topics"],
      properties: {
        session_id: {
          bsonType: "string"
        },
        user_id: {
          bsonType: "string"
        },
        performance_metrics: {
          bsonType: "object"
        },
        strength_areas: {
          bsonType: "array"
        },
        improvement_areas: {
          bsonType: "array"
        },
        detailed_feedback: {
          bsonType: "string",
          minLength: 1
        },
        recommended_practice_topics: {
          bsonType: "array"
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": 1 });
db.users.createIndex({ "is_active": 1 });

db.resumes.createIndex({ "user_id": 1 });
db.resumes.createIndex({ "created_at": 1 });
db.resumes.createIndex({ "is_processed": 1 });

db.interview_sessions.createIndex({ "user_id": 1 });
db.interview_sessions.createIndex({ "created_at": 1 });
db.interview_sessions.createIndex({ "is_completed": 1 });
db.interview_sessions.createIndex({ "job_role": 1 });

db.feedback_reports.createIndex({ "session_id": 1 }, { unique: true });
db.feedback_reports.createIndex({ "user_id": 1 });
db.feedback_reports.createIndex({ "created_at": 1 });

// Create admin user (default password: admin123)
db.users.insertOne({
  email: "admin@interviewai.com",
  name: "System Admin",
  role: "admin",
  hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",
  is_active: true,
  created_at: new Date(),
  updated_at: new Date()
});

print("Database initialized successfully");
