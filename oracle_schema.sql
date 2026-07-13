-- =============================================================================
--  GapInsight – Research Gap Detection & Recommendation System
--  FILE 1: Oracle Database Schema  (CSC371 – Database Systems)
--  Student: Kashaf Fayyaz | FA24-BAI-028
-- =============================================================================
--  HOW TO RUN:
--    1. Open Oracle SQL Developer
--    2. Connect to your Oracle database
--    3. Open this file → Run Script (F5)
-- =============================================================================

-- Clean slate: drop everything first (safe to re-run)
BEGIN
  FOR t IN (
    SELECT table_name FROM user_tables
    WHERE table_name IN (
      'USERS','USER_PROFILE','STUDENT','RESEARCHER','ADMIN_USER',
      'RESEARCH_ASSISTANT','REVIEWER','AUTHOR','EXTERNAL_EXPERT',
      'CONTRIBUTOR','CATEGORIES','BOOKMARKS','ACTIVITY_LOG',
      'RECOMMENDATIONS','PAPER_AUTHOR','RESEARCH_GAPS'
    )
  ) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/

BEGIN
  FOR s IN (
    SELECT sequence_name FROM user_sequences
    WHERE sequence_name IN (
      'SEQ_USER','SEQ_PROFILE','SEQ_CATEGORY','SEQ_BOOKMARK',
      'SEQ_LOG','SEQ_RECOMMENDATION','SEQ_AUTHOR','SEQ_EXPERT',
      'SEQ_GAP'
    )
  ) LOOP
    EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
  END LOOP;
END;
/


-- =============================================================================
--  SEQUENCES  (auto-increment IDs for Oracle)
-- =============================================================================

CREATE SEQUENCE SEQ_USER          START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_PROFILE       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_CATEGORY      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_BOOKMARK      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_LOG           START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_RECOMMENDATION START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_AUTHOR        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_EXPERT        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_GAP           START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;


-- =============================================================================
--  CORE TABLES
-- =============================================================================

-- -----------------------------------------------------------------------------
--  USERS  (Superclass)
--  Stores every person who logs into the system.
-- -----------------------------------------------------------------------------
CREATE TABLE Users (
    user_id       NUMBER         PRIMARY KEY,
    name          VARCHAR2(100)  NOT NULL,
    email         VARCHAR2(150)  UNIQUE NOT NULL,
    password_hash VARCHAR2(256)  NOT NULL,          -- store hashed, never plain text
    role          VARCHAR2(20)   NOT NULL
                  CHECK (role IN ('Student','Researcher','Admin','Reviewer')),
    created_at    DATE           DEFAULT SYSDATE,
    is_active     NUMBER(1)      DEFAULT 1 CHECK (is_active IN (0,1))
);

COMMENT ON TABLE  Users            IS 'Superclass: every system user';
COMMENT ON COLUMN Users.role       IS 'Disjoint specialisation: one primary role per user';
COMMENT ON COLUMN Users.password_hash IS 'SHA-256 hash — never store plain passwords';


-- -----------------------------------------------------------------------------
--  USER_PROFILE  (1:1 with Users)
-- -----------------------------------------------------------------------------
CREATE TABLE User_Profile (
    profile_id        NUMBER        PRIMARY KEY,
    user_id           NUMBER        UNIQUE NOT NULL,
    university        VARCHAR2(200),
    department        VARCHAR2(100),
    research_interest VARCHAR2(500),
    bio               VARCHAR2(1000),
    profile_pic_url   VARCHAR2(300),
    CONSTRAINT fk_profile_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE User_Profile IS '1:1 extension of Users with academic details';


-- -----------------------------------------------------------------------------
--  CATEGORIES  (Research domains — e.g. "Machine Learning", "NLP")
-- -----------------------------------------------------------------------------
CREATE TABLE Categories (
    category_id   NUMBER         PRIMARY KEY,
    name          VARCHAR2(100)  UNIQUE NOT NULL,
    description   VARCHAR2(500),
    parent_id     NUMBER,                          -- self-referencing for sub-domains
    created_at    DATE           DEFAULT SYSDATE,
    CONSTRAINT fk_cat_parent FOREIGN KEY (parent_id) REFERENCES Categories(category_id)
);

COMMENT ON TABLE  Categories           IS 'Research domain taxonomy with optional hierarchy';
COMMENT ON COLUMN Categories.parent_id IS 'NULL = top-level domain; NOT NULL = sub-domain';


-- =============================================================================
--  EER SUBCLASS TABLES  (Disjoint Specialisation)
-- =============================================================================

-- -----------------------------------------------------------------------------
--  STUDENT  (Subclass of Users)
-- -----------------------------------------------------------------------------
CREATE TABLE Student (
    user_id         NUMBER        PRIMARY KEY,
    student_reg_no  VARCHAR2(30)  UNIQUE NOT NULL,
    degree_program  VARCHAR2(100),
    semester        NUMBER(2),
    CONSTRAINT fk_student_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE Student IS 'EER Subclass of Users (disjoint). Extra student attributes.';


-- -----------------------------------------------------------------------------
--  RESEARCHER  (Subclass of Users)
-- -----------------------------------------------------------------------------
CREATE TABLE Researcher (
    user_id          NUMBER        PRIMARY KEY,
    research_area    VARCHAR2(200) NOT NULL,
    institution      VARCHAR2(200),
    h_index          NUMBER(5)     DEFAULT 0,
    publications_cnt NUMBER(6)     DEFAULT 0,
    CONSTRAINT fk_researcher_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE Researcher IS 'EER Subclass of Users (disjoint). Extra researcher attributes.';


-- -----------------------------------------------------------------------------
--  ADMIN_USER  (Subclass of Users)
-- -----------------------------------------------------------------------------
CREATE TABLE Admin_User (
    user_id     NUMBER        PRIMARY KEY,
    permissions VARCHAR2(500) DEFAULT 'read,write',   -- comma-separated permission list
    last_login  DATE,
    CONSTRAINT fk_admin_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE Admin_User IS 'EER Subclass of Users (disjoint). System administration role.';


-- =============================================================================
--  EER: MULTIPLE INHERITANCE
--  ResearchAssistant inherits from BOTH Student AND Researcher
-- =============================================================================
CREATE TABLE Research_Assistant (
    user_id         NUMBER       PRIMARY KEY,
    supervisor_id   NUMBER,                          -- points to a Researcher
    stipend_amount  NUMBER(10,2) DEFAULT 0,
    start_date      DATE,
    CONSTRAINT fk_ra_user       FOREIGN KEY (user_id)
        REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_ra_student    FOREIGN KEY (user_id)
        REFERENCES Student(user_id),                 -- inherits Student
    CONSTRAINT fk_ra_supervisor FOREIGN KEY (supervisor_id)
        REFERENCES Researcher(user_id)
);

COMMENT ON TABLE Research_Assistant IS
    'EER Multiple Inheritance: ResearchAssistant IS-A Student AND IS-A Researcher';


-- =============================================================================
--  EER: OVERLAPPING SPECIALISATION
--  A user can be both Author AND Reviewer (overlapping, not disjoint)
-- =============================================================================

-- -----------------------------------------------------------------------------
--  AUTHOR  (Overlapping subclass — internal author who is also a User)
-- -----------------------------------------------------------------------------
CREATE TABLE Author (
    author_id    NUMBER        PRIMARY KEY,
    user_id      NUMBER,                            -- NULL if external author
    name         VARCHAR2(150) NOT NULL,
    affiliation  VARCHAR2(200),
    email        VARCHAR2(150),
    orcid_id     VARCHAR2(30),                      -- researcher unique ID
    CONSTRAINT fk_author_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE SET NULL
);

COMMENT ON TABLE Author IS
    'EER Overlapping: a User CAN also be an Author (and/or a Reviewer)';


-- -----------------------------------------------------------------------------
--  REVIEWER  (Overlapping subclass)
-- -----------------------------------------------------------------------------
CREATE TABLE Reviewer (
    user_id           NUMBER       PRIMARY KEY,
    expertise_area    VARCHAR2(200),
    reviews_completed NUMBER(6)    DEFAULT 0,
    rating            NUMBER(3,2)  DEFAULT 0.00
                      CHECK (rating BETWEEN 0 AND 5),
    CONSTRAINT fk_reviewer_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE Reviewer IS
    'EER Overlapping: a User CAN also be a Reviewer (and/or an Author)';


-- =============================================================================
--  EER: UNION TYPE (Category / UNION)
--  Contributor = Internal User OR External Expert
-- =============================================================================

-- -----------------------------------------------------------------------------
--  EXTERNAL_EXPERT  (non-system user who contributes papers)
-- -----------------------------------------------------------------------------
CREATE TABLE External_Expert (
    expert_id    NUMBER        PRIMARY KEY,
    name         VARCHAR2(150) NOT NULL,
    email        VARCHAR2(150) UNIQUE,
    organization VARCHAR2(200),
    country      VARCHAR2(100)
);

COMMENT ON TABLE External_Expert IS 'Part of UNION type Contributor (external side)';


-- -----------------------------------------------------------------------------
--  CONTRIBUTOR  (Union of Users and External_Expert)
--  Exactly one of (user_id, expert_id) will be NOT NULL per row.
-- -----------------------------------------------------------------------------
CREATE TABLE Contributor (
    contributor_id NUMBER       PRIMARY KEY,
    user_id        NUMBER,                         -- set if internal user
    expert_id      NUMBER,                         -- set if external expert
    contribution   VARCHAR2(500),
    contributed_on DATE DEFAULT SYSDATE,
    CONSTRAINT fk_contrib_user   FOREIGN KEY (user_id)   REFERENCES Users(user_id)   ON DELETE CASCADE,
    CONSTRAINT fk_contrib_expert FOREIGN KEY (expert_id) REFERENCES External_Expert(expert_id) ON DELETE CASCADE,
    -- Enforce UNION: exactly one side must be populated
    CONSTRAINT chk_union_type CHECK (
        (user_id IS NOT NULL AND expert_id IS NULL) OR
        (user_id IS NULL     AND expert_id IS NOT NULL)
    )
);

COMMENT ON TABLE Contributor IS
    'EER UNION TYPE: Contributor is either an internal User OR an External Expert, never both';


-- =============================================================================
--  MANY-TO-MANY: Paper ↔ Author
--  paper_id is a VARCHAR2 because it references MongoDB's ObjectId
-- =============================================================================
CREATE TABLE Paper_Author (
    paper_id     VARCHAR2(30)  NOT NULL,    -- MongoDB ObjectId stored as string
    author_id    NUMBER        NOT NULL,
    is_primary   NUMBER(1)     DEFAULT 0 CHECK (is_primary IN (0,1)),
    author_order NUMBER(3)     DEFAULT 1,
    CONSTRAINT pk_paper_author PRIMARY KEY (paper_id, author_id),
    CONSTRAINT fk_pa_author    FOREIGN KEY (author_id) REFERENCES Author(author_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE  Paper_Author          IS 'M:N bridge between MongoDB papers and Oracle authors';
COMMENT ON COLUMN Paper_Author.paper_id IS 'MongoDB ObjectId — FK to MongoDB Papers collection';


-- =============================================================================
--  BOOKMARKS  (User saves a paper — 1:M with total participation on Bookmark side)
-- =============================================================================
CREATE TABLE Bookmarks (
    bookmark_id  NUMBER        PRIMARY KEY,
    user_id      NUMBER        NOT NULL,    -- total participation: every bookmark MUST have a user
    paper_id     VARCHAR2(30)  NOT NULL,    -- MongoDB ObjectId
    saved_at     DATE          DEFAULT SYSDATE,
    notes        VARCHAR2(500),
    CONSTRAINT fk_bm_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT uq_bm_user_paper UNIQUE (user_id, paper_id)
);

COMMENT ON TABLE  Bookmarks         IS 'Total participation: every Bookmark MUST belong to a User';
COMMENT ON COLUMN Bookmarks.user_id IS 'NOT NULL enforces total participation constraint';


-- =============================================================================
--  ACTIVITY_LOG  (Audit trail — 1:M User to Logs)
-- =============================================================================
CREATE TABLE Activity_Log (
    log_id      NUMBER        PRIMARY KEY,
    user_id     NUMBER        NOT NULL,
    action      VARCHAR2(100) NOT NULL,      -- e.g. 'SEARCH', 'UPLOAD', 'BOOKMARK'
    detail      VARCHAR2(500),               -- extra detail, e.g. search query
    ip_address  VARCHAR2(45),
    logged_at   DATE          DEFAULT SYSDATE,
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

COMMENT ON TABLE Activity_Log IS '1:M audit log. Every action tracked per user.';


-- =============================================================================
--  RECOMMENDATIONS  (System-generated research recommendations per user)
-- =============================================================================
CREATE TABLE Recommendations (
    recommendation_id NUMBER       PRIMARY KEY,
    user_id           NUMBER       NOT NULL,
    topic             VARCHAR2(200) NOT NULL,
    score             NUMBER(5,4)   CHECK (score BETWEEN 0 AND 1),  -- 0.0 to 1.0
    category_id       NUMBER,
    reason            VARCHAR2(500),
    generated_at      DATE         DEFAULT SYSDATE,
    is_viewed         NUMBER(1)    DEFAULT 0 CHECK (is_viewed IN (0,1)),
    CONSTRAINT fk_rec_user     FOREIGN KEY (user_id)     REFERENCES Users(user_id)     ON DELETE CASCADE,
    CONSTRAINT fk_rec_category FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

COMMENT ON TABLE Recommendations IS 'AI-generated research topic recommendations per user';


-- =============================================================================
--  RESEARCH_GAPS  (Detected gaps stored here after analysis)
-- =============================================================================
CREATE TABLE Research_Gaps (
    gap_id          NUMBER        PRIMARY KEY,
    category_id     NUMBER        NOT NULL,
    keyword         VARCHAR2(200) NOT NULL,
    paper_count     NUMBER(8)     DEFAULT 0,   -- how many papers cover this topic
    gap_score       NUMBER(5,4)   CHECK (gap_score BETWEEN 0 AND 1), -- 1 = total gap
    detected_on     DATE          DEFAULT SYSDATE,
    description     VARCHAR2(1000),
    CONSTRAINT fk_gap_category FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

COMMENT ON TABLE Research_Gaps IS 'Results of gap detection analysis — low paper_count = bigger gap';


-- =============================================================================
--  INDEXES  (for fast lookups on commonly queried columns)
-- =============================================================================

CREATE INDEX idx_users_email       ON Users(email);
CREATE INDEX idx_users_role        ON Users(role);
CREATE INDEX idx_profile_user      ON User_Profile(user_id);
CREATE INDEX idx_bookmark_user     ON Bookmarks(user_id);
CREATE INDEX idx_bookmark_paper    ON Bookmarks(paper_id);
CREATE INDEX idx_log_user          ON Activity_Log(user_id);
CREATE INDEX idx_log_action        ON Activity_Log(action);
CREATE INDEX idx_rec_user          ON Recommendations(user_id);
CREATE INDEX idx_rec_score         ON Recommendations(score DESC);
CREATE INDEX idx_gap_category      ON Research_Gaps(category_id);
CREATE INDEX idx_gap_score         ON Research_Gaps(gap_score DESC);
CREATE INDEX idx_paper_author_pid  ON Paper_Author(paper_id);
CREATE INDEX idx_paper_author_aid  ON Paper_Author(author_id);


-- =============================================================================
--  TRIGGERS  (auto-populate primary keys from sequences)
-- =============================================================================

CREATE OR REPLACE TRIGGER trg_users_id
BEFORE INSERT ON Users FOR EACH ROW
BEGIN IF :NEW.user_id IS NULL THEN :NEW.user_id := SEQ_USER.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_profile_id
BEFORE INSERT ON User_Profile FOR EACH ROW
BEGIN IF :NEW.profile_id IS NULL THEN :NEW.profile_id := SEQ_PROFILE.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_category_id
BEFORE INSERT ON Categories FOR EACH ROW
BEGIN IF :NEW.category_id IS NULL THEN :NEW.category_id := SEQ_CATEGORY.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_bookmark_id
BEFORE INSERT ON Bookmarks FOR EACH ROW
BEGIN IF :NEW.bookmark_id IS NULL THEN :NEW.bookmark_id := SEQ_BOOKMARK.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_log_id
BEFORE INSERT ON Activity_Log FOR EACH ROW
BEGIN IF :NEW.log_id IS NULL THEN :NEW.log_id := SEQ_LOG.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_rec_id
BEFORE INSERT ON Recommendations FOR EACH ROW
BEGIN IF :NEW.recommendation_id IS NULL THEN :NEW.recommendation_id := SEQ_RECOMMENDATION.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_author_id
BEFORE INSERT ON Author FOR EACH ROW
BEGIN IF :NEW.author_id IS NULL THEN :NEW.author_id := SEQ_AUTHOR.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_expert_id
BEFORE INSERT ON External_Expert FOR EACH ROW
BEGIN IF :NEW.expert_id IS NULL THEN :NEW.expert_id := SEQ_EXPERT.NEXTVAL; END IF; END;
/

CREATE OR REPLACE TRIGGER trg_gap_id
BEFORE INSERT ON Research_Gaps FOR EACH ROW
BEGIN IF :NEW.gap_id IS NULL THEN :NEW.gap_id := SEQ_GAP.NEXTVAL; END IF; END;
/

-- Log every new user registration automatically
CREATE OR REPLACE TRIGGER trg_log_new_user
AFTER INSERT ON Users FOR EACH ROW
BEGIN
    INSERT INTO Activity_Log (user_id, action, detail)
    VALUES (:NEW.user_id, 'REGISTER', 'New account created: ' || :NEW.email);
END;
/


-- =============================================================================
--  STORED PROCEDURES
-- =============================================================================

-- Register a new user (creates User + Profile + subclass row in one call)
CREATE OR REPLACE PROCEDURE sp_register_user (
    p_name          IN VARCHAR2,
    p_email         IN VARCHAR2,
    p_password_hash IN VARCHAR2,
    p_role          IN VARCHAR2,
    p_university    IN VARCHAR2 DEFAULT NULL,
    p_research_int  IN VARCHAR2 DEFAULT NULL,
    p_student_reg   IN VARCHAR2 DEFAULT NULL,
    p_new_user_id   OUT NUMBER
) AS
BEGIN
    -- Insert into Users
    INSERT INTO Users (name, email, password_hash, role)
    VALUES (p_name, p_email, p_password_hash, p_role)
    RETURNING user_id INTO p_new_user_id;

    -- Insert profile
    INSERT INTO User_Profile (user_id, university, research_interest)
    VALUES (p_new_user_id, p_university, p_research_int);

    -- Insert subclass row based on role
    IF p_role = 'Student' THEN
        INSERT INTO Student (user_id, student_reg_no)
        VALUES (p_new_user_id, NVL(p_student_reg, 'REG-' || p_new_user_id));
    ELSIF p_role = 'Researcher' THEN
        INSERT INTO Researcher (user_id, research_area)
        VALUES (p_new_user_id, NVL(p_research_int, 'General'));
    ELSIF p_role = 'Admin' THEN
        INSERT INTO Admin_User (user_id) VALUES (p_new_user_id);
    END IF;

    COMMIT;
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Email already registered: ' || p_email);
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_register_user;
/


-- Get top N recommendations for a user
CREATE OR REPLACE PROCEDURE sp_get_recommendations (
    p_user_id IN NUMBER,
    p_limit   IN NUMBER DEFAULT 5,
    p_cursor  OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT r.topic, r.score, r.reason, c.name AS category,
               r.generated_at
        FROM   Recommendations r
        LEFT JOIN Categories c ON r.category_id = c.category_id
        WHERE  r.user_id   = p_user_id
        ORDER  BY r.score  DESC
        FETCH  FIRST p_limit ROWS ONLY;
END sp_get_recommendations;
/


-- =============================================================================
--  VIEWS  (useful pre-built queries)
-- =============================================================================

-- Full user info joined with profile
CREATE OR REPLACE VIEW vw_user_full AS
SELECT u.user_id, u.name, u.email, u.role, u.created_at, u.is_active,
       p.university, p.department, p.research_interest, p.bio
FROM   Users u
LEFT JOIN User_Profile p ON u.user_id = p.user_id;

-- Top research gaps (sorted by gap score descending)
CREATE OR REPLACE VIEW vw_top_gaps AS
SELECT g.gap_id, g.keyword, g.gap_score, g.paper_count,
       c.name AS category, g.detected_on, g.description
FROM   Research_Gaps g
JOIN   Categories c ON g.category_id = c.category_id
ORDER  BY g.gap_score DESC;

-- User activity summary
CREATE OR REPLACE VIEW vw_user_activity AS
SELECT u.user_id, u.name, u.email,
       COUNT(l.log_id)                                   AS total_actions,
       COUNT(CASE WHEN l.action='SEARCH'   THEN 1 END)   AS searches,
       COUNT(CASE WHEN l.action='UPLOAD'   THEN 1 END)   AS uploads,
       COUNT(CASE WHEN l.action='BOOKMARK' THEN 1 END)   AS bookmarks,
       MAX(l.logged_at)                                  AS last_active
FROM   Users u
LEFT JOIN Activity_Log l ON u.user_id = l.user_id
GROUP  BY u.user_id, u.name, u.email;

-- Papers per author (cross-DB bridge view)
CREATE OR REPLACE VIEW vw_author_papers AS
SELECT a.author_id, a.name, a.affiliation,
       COUNT(pa.paper_id) AS paper_count,
       LISTAGG(pa.paper_id, ', ')
           WITHIN GROUP (ORDER BY pa.paper_id) AS paper_ids
FROM   Author a
LEFT JOIN Paper_Author pa ON a.author_id = pa.author_id
GROUP  BY a.author_id, a.name, a.affiliation;


-- =============================================================================
--  SAMPLE DATA  (enough to test every table)
-- =============================================================================

-- Categories
INSERT INTO Categories (name, description) VALUES ('Machine Learning', 'ML algorithms and applications');
INSERT INTO Categories (name, description) VALUES ('Natural Language Processing', 'Text and language AI');
INSERT INTO Categories (name, description) VALUES ('Computer Vision', 'Image and video processing');
INSERT INTO Categories (name, description, parent_id) VALUES ('Deep Learning', 'Neural network architectures', 1);
INSERT INTO Categories (name, description, parent_id) VALUES ('Transformers', 'Attention-based NLP models', 2);

-- Users
DECLARE v_id NUMBER;
BEGIN
    sp_register_user('Kashaf Fayyaz',  'kashaf@uni.edu',   'hash_kashaf',  'Student',    'FAST NUCES', 'AI & ML',        'FA24-BAI-028', v_id);
    sp_register_user('Dr. Shahid Ali', 'shahid@uni.edu',   'hash_shahid',  'Researcher', 'FAST NUCES', 'Database Systems', NULL,          v_id);
    sp_register_user('Sara Ahmed',     'sara@uni.edu',     'hash_sara',    'Student',    'LUMS',       'NLP',             'FA24-CS-045',  v_id);
    sp_register_user('Admin User',     'admin@gapinsight.com','hash_admin','Admin',      NULL,         NULL,              NULL,           v_id);
END;
/

-- Authors (one internal, one external)
INSERT INTO Author (name, affiliation, email, user_id) VALUES ('Kashaf Fayyaz', 'FAST NUCES', 'kashaf@uni.edu', 1);
INSERT INTO Author (name, affiliation, email, user_id) VALUES ('Dr. Shahid Ali','FAST NUCES', 'shahid@uni.edu', 2);
INSERT INTO Author (name, affiliation, email, user_id) VALUES ('Sara Ahmed',    'LUMS',       'sara@uni.edu',   3);

-- External Expert
INSERT INTO External_Expert (name, email, organization, country)
VALUES ('Dr. Andrew Ng', 'andrew@deeplearning.ai', 'DeepLearning.AI', 'USA');

-- Reviewer
INSERT INTO Reviewer (user_id, expertise_area) VALUES (2, 'Database Systems, AI');

-- Bookmarks (paper_id = MongoDB ObjectId placeholder)
INSERT INTO Bookmarks (user_id, paper_id, notes) VALUES (1, '64f1a2b3c4d5e6f708091011', 'Great paper on RAG');
INSERT INTO Bookmarks (user_id, paper_id, notes) VALUES (1, '64f1a2b3c4d5e6f708091012', 'Related to my project');
INSERT INTO Bookmarks (user_id, paper_id, notes) VALUES (3, '64f1a2b3c4d5e6f708091011', 'For NLP research');

-- Activity Logs
INSERT INTO Activity_Log (user_id, action, detail) VALUES (1, 'SEARCH',   'Query: research gap detection NLP');
INSERT INTO Activity_Log (user_id, action, detail) VALUES (1, 'UPLOAD',   'Uploaded: transformer_survey.pdf');
INSERT INTO Activity_Log (user_id, action, detail) VALUES (1, 'BOOKMARK', 'Bookmarked paper: 64f1a2b3c4d5e6f708091011');
INSERT INTO Activity_Log (user_id, action, detail) VALUES (3, 'SEARCH',   'Query: BERT fine tuning');

-- Recommendations
INSERT INTO Recommendations (user_id, topic, score, category_id, reason)
VALUES (1, 'Multimodal Learning Research Gaps', 0.92, 1, 'Low paper count despite high citation demand');
INSERT INTO Recommendations (user_id, topic, score, category_id, reason)
VALUES (1, 'Low-Resource NLP for Urdu', 0.88, 2, 'Very few published papers in this area');
INSERT INTO Recommendations (user_id, topic, score, category_id, reason)
VALUES (3, 'Efficient Transformers for Edge Devices', 0.85, 5, 'Emerging topic with few comprehensive surveys');

-- Research Gaps
INSERT INTO Research_Gaps (category_id, keyword, paper_count, gap_score, description)
VALUES (2, 'Urdu NLP', 12, 0.91, 'Severely under-researched despite large speaker base');
INSERT INTO Research_Gaps (category_id, keyword, paper_count, gap_score, description)
VALUES (1, 'Federated Learning Privacy', 34, 0.78, 'Privacy aspects of federated ML need more focus');
INSERT INTO Research_Gaps (category_id, keyword, paper_count, gap_score, description)
VALUES (3, 'Medical Image Segmentation 3D', 28, 0.72, '3D MRI segmentation remains a challenge');

-- Paper_Author links (MongoDB paper IDs)
INSERT INTO Paper_Author (paper_id, author_id, is_primary, author_order)
VALUES ('64f1a2b3c4d5e6f708091011', 1, 1, 1);
INSERT INTO Paper_Author (paper_id, author_id, is_primary, author_order)
VALUES ('64f1a2b3c4d5e6f708091011', 2, 0, 2);
INSERT INTO Paper_Author (paper_id, author_id, is_primary, author_order)
VALUES ('64f1a2b3c4d5e6f708091012', 3, 1, 1);

COMMIT;


-- =============================================================================
--  VERIFICATION QUERIES  (run these to confirm everything works)
-- =============================================================================

-- Check all tables were created
SELECT table_name FROM user_tables ORDER BY table_name;

-- Check users
SELECT * FROM vw_user_full;

-- Check top gaps
SELECT * FROM vw_top_gaps;

-- Check activity summary
SELECT * FROM vw_user_activity;

-- Check EER subclass tables
SELECT u.name, u.role, s.student_reg_no, s.degree_program
FROM Users u JOIN Student s ON u.user_id = s.user_id;

SELECT u.name, u.role, r.research_area, r.h_index
FROM Users u JOIN Researcher r ON u.user_id = r.user_id;

-- Check union type constraint works
-- This should FAIL (both user_id and expert_id set):
-- INSERT INTO Contributor (contributor_id, user_id, expert_id, contribution)
-- VALUES (1, 1, 1, 'test');   -- <-- violates CHECK constraint

PROMPT ============================================================
PROMPT  GapInsight Oracle Schema loaded successfully!
PROMPT  Tables: 16  |  Indexes: 13  |  Triggers: 10  |  Views: 4
PROMPT ============================================================