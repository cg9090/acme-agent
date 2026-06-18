-- USERS
INSERT INTO users (username, role_name)
VALUES
('alice', 'sales_user'),
('bob', 'support_user'),
('admin', 'admin');

-- CUSTOMERS
INSERT INTO customers (name, industry, account_owner)
VALUES
('Globex Manufacturing', 'Manufacturing', 'Alice'),
('Initech Solutions', 'Technology', 'Bob'),
('Umbrella Healthcare', 'Healthcare', 'Charlie');

-- ISSUES
INSERT INTO issues (customer_id, title, description, status, priority)
VALUES
(
1,
'API integration failures',
'Customer reports intermittent failures when submitting orders through the public API. Failures increased after the latest platform release.',
'OPEN',
'HIGH'
),
(
1,
'Invoice processing delays',
'Invoices are taking significantly longer than expected to process, causing delays to customer billing workflows.',
'OPEN',
'MEDIUM'
),
(
2,
'SSO login failures',
'Several users are unable to authenticate via single sign-on. Issue appears to affect users provisioned within the last month.',
'OPEN',
'HIGH'
),
(
2,
'Reporting dashboard timeout',
'Dashboard reports are timing out during peak business hours when large datasets are queried.',
'OPEN',
'MEDIUM'
),
(
3,
'Data export timeout',
'Large data exports were timing out for enterprise customers.',
'CLOSED',
'LOW'
);

-- ISSUE UPDATES
INSERT INTO issue_updates (issue_id, update_text)
VALUES
(1, 'Customer provided API request logs showing authentication failures.'),
(1, 'Engineering identified token expiry validation issue.'),
(1, 'Patch created and currently undergoing QA testing.'),

(2, 'Database team reviewing invoice processing pipeline.'),
(2, 'Potential indexing issue identified.'),

(3, 'Issue reproduced successfully in staging environment.'),
(3, 'Misconfigured identity provider mapping discovered.'),
(3, 'Configuration fix deployed and awaiting customer confirmation.'),

(4, 'Performance bottleneck isolated to reporting query execution.'),
(4, 'Optimisation recommendations prepared by engineering.'),

(5, 'Infrastructure scaling completed.'),
(5, 'Customer confirmed export functionality is operating normally.');

-- NEXT ACTIONS
INSERT INTO next_actions (issue_id, action_text, created_by)
VALUES
(
1,
'Deploy authentication patch to staging and arrange customer validation session.',
'admin'
),
(
2,
'Implement database indexing improvements and monitor processing times.',
'bob'
),
(
3,
'Obtain customer sign-off and close issue if validation succeeds.',
'admin'
),
(
4,
'Implement query optimisation changes during the next maintenance window.',
'bob'
),
(
5,
'No further action required. Continue routine monitoring.',
'admin'
);
