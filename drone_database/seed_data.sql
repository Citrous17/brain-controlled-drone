INSERT INTO users (username, email) VALUES
('neuro_explorer', 'neuro1@TeamMegamind.com'),
('brain_hacker', 'brainhacker@TeamMegamind.com'),
('mind_reader', 'mindreader@TeamMegamind.com');

INSERT INTO sessions (user_id, session_name, start_time, end_time) VALUES
(1, 'Session 1', '2025-03-02 08:00:00', '2025-03-02 08:30:00'),
(1, 'Session 2', '2025-03-02 18:00:00', '2025-03-02 18:45:00'),
(2, 'Session 1', '2025-03-02 22:00:00', '2025-03-02 06:00:00'),
(3, 'Session 1', '2025-03-02 14:00:00', '2025-03-02 14:45:00');

INSERT INTO brainwave_data (session_id, timestamp, alpha, beta, theta, delta, gamma, raw_data) VALUES
(1, '2025-03-02 08:01:00', 5.2, 3.1, 2.5, 1.8, 0.9, '{"signal": [0.1, 0.2, 0.3]}'),
(1, '2025-03-02 08:02:00', 5.5, 3.3, 2.8, 2.0, 1.0, '{"signal": [0.2, 0.3, 0.4]}'),
(2, '2025-03-02 18:01:00', 6.0, 4.0, 3.2, 1.9, 1.2, '{"signal": [0.3, 0.4, 0.5]}'),
(3, '2025-03-02 22:10:00', 2.2, 1.5, 5.8, 6.9, 0.5, '{"signal": [0.2, 0.1, 0.3]}'),
(4, '2025-03-02 14:05:00', 4.8, 5.0, 2.1, 2.0, 3.2, '{"signal": [0.5, 0.6, 0.7]}');

INSERT INTO brainwave_metrics (session_id, alpha_avg, beta_avg, theta_avg, delta_avg, gamma_avg, session_duration) VALUES
(1, 5.3, 3.2, 2.65, 1.9, 0.95, 1800), 
(2, 6.0, 4.0, 3.2, 1.9, 1.2, 2700), 
(3, 2.2, 1.5, 5.8, 6.9, 0.5, 28800),
(4, 4.8, 5.0, 2.1, 2.0, 3.2, 2700);
