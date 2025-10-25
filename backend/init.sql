-- Task table with improved schema design
CREATE TABLE IF NOT EXISTS task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    priority ENUM('low', 'normal', 'urgent') DEFAULT 'normal' NOT NULL,
    due_date DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    
    -- Constraints
    CONSTRAINT chk_title_not_empty CHECK (CHAR_LENGTH(TRIM(title)) > 0),
    
    -- Indexes for performance
    INDEX idx_completed (completed),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_completed_created (completed, created_at DESC),
    INDEX idx_due_date (due_date),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


