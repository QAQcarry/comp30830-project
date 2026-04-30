
# Generative AI Report
# 25206899 Wenfei Song


## Sprint 1:

1. After interviewing users, the requirements collected were very fragmented. Even with the template provided by the instructor, it was still unclear how to begin organizing them into user stories.

* **I asked AI:** I have a large number of disorganized user requirements. How can I write them in a proper User Story format?
* **AI told me:** It provided the classic template `As a [role], I want to [action], so that [value]`. It helped transform informal interview content into professional agile requirements, and further suggested using Trello or Jira to manage these tasks.

2. During AWS EC2 configuration, some options did not exactly match the screenshots provided in the lab, and I was concerned about selecting the wrong options and incurring charges. I asked AI about the meaning of each option and how to properly set up the instance.

* **I asked AI:** The current AWS EC2 setup interface is different from the tutorial. How can I ensure that my configuration stays entirely within the free tier?
* **AI told me:** It is necessary to strictly select options labeled "Free tier eligible". In the Amazon Machine Image option, choose Ubuntu Server 22.04 LTS or 24.04 LTS. In the instance type option, strictly select `t2.micro` or `t3.micro` depending on the region. Leave advanced monitoring and Elastic IP options disabled by default to avoid additional charges.

3. In the Network settings section, I encountered complex concepts such as VPC, subnet, public IP, and security groups, and was unsure how to configure them to allow external access to the website.

* **I asked AI:** What do the different network settings and security group options represent, and how should they be configured to allow external access and remote login?
* **AI told me:**
  1. Public IP: Ensure that Auto assign public IP is set to Enable, otherwise the instance will not have an external address.
  2. Security Group: This acts as a cloud firewall. Inbound rules must allow port 22 for SSH access, and ports 80 and 443 for HTTP and HTTPS web access.

4. In the final stage of configuration, the system required selecting or creating a key pair. I was unsure about its purpose, which format to choose, and how to use it to connect to the instance.

* **I asked AI:** What is the purpose of a key pair? Should I choose RSA or ED25519? How do I use it to log into the server after downloading it?
* **AI told me:** A key pair is a secure credential that replaces password based login. It is recommended to choose the RSA algorithm and the `.pem` format. After creation, the `.pem` file must be stored securely, as losing it will prevent access to the instance. After launching the instance, run `chmod 400 keyname.pem` in the local terminal to set read only permission, then connect using `ssh -i "keyname.pem" ubuntu@public_ip`.

---

## Sprint 2:

1. After writing database connection code locally, no changes appeared in the Source Control panel in VS Code, and I could not push code to GitHub through the interface.

* **I asked AI:** I modified files, but no changes appear in VS Code Source Control. How can I push my code to GitHub?
* **AI told me:** This may be due to VS Code not refreshing or not opening the correct folder containing the `.git` directory. It suggested using the command line directly by running `git status`, `git add .`, `git commit -m "message"`, and `git push origin main`.

2. The MySQL database was deployed on my EC2 instance, and my teammate needed to run a crawler locally and write data into this database. I did not know how to configure remote access.

* **I asked AI:** The database is on EC2, and my teammate runs code locally. How should the database connection be configured?
* **AI told me:** It provided the standard connection string format `mysql+pymysql://username:password@EC2_public_ip:3306/dbname`. It also emphasized that port 3306 should only be opened to the teammate's local IP in the AWS security group inbound rules, and not set to `0.0.0.0/0` to avoid security risks.

---

## Sprint 3:

1. This week I acted as the master and needed to use Jira for agile management. I had to assign tasks to teammates via email, but could not find an option to assign tasks directly by email in the ticket interface.

* **I asked AI:** How can I create tasks in Jira and assign them to teammates using email?
* **AI told me:** Jira does not allow assigning tasks directly by entering an email address in the ticket interface. You must first go to Project Settings and then People or Team, invite teammates by email to join the project, and after they accept, assign tasks to them through the Assignee field.

2. While testing crawler data submitted by teammates, the backend returned an HTTP 500 error, and the terminal log showed `KeyError: 'available_bikes'` and `TypeError: 'NoneType' object is not iterable`.

* **I asked AI:** The backend returns a 500 error with KeyError and TypeError when processing crawler data. How should this be handled?
* **AI told me:** The issue is caused by missing fields or null values in the incoming data. It recommended defensive programming. Use `data.get('available_bikes', 0)` instead of direct indexing to avoid KeyError, and check `if not data:` before iteration or use try except blocks to prevent crashes due to invalid data.

3. I added a Flask route `@app.route('/api/weather')`, but accessing it in the browser resulted in a 404 Not Found error.

* **I asked AI:** The route function is added and there are no errors in the code. Why does accessing the endpoint return 404?
* **AI told me:** This happens because the project uses Flask Blueprints. In modular files, you should use `@bp.route` instead of `@app.route`, and ensure that the blueprint is properly registered in the main application using `register_blueprint()`.

---

## Sprint 4:

1. When testing locally, loading the model using `joblib.load('model.pkl')` worked correctly. However, after deploying to the EC2 server and running Flask, a `FileNotFoundError` occurred.

* **I asked AI:** The model file can be found locally, but not on the server. How can I fix the path issue?
* **AI told me:** This is because relative paths depend on the current working directory, which may differ between environments. It suggested using the `os` module and constructing an absolute path with `os.path.join(os.path.dirname(__file__), 'model.pkl')`.

2. The model requires specific input features such as current hour, day of the week, and real time temperature. I did not know how to dynamically obtain and format this data in the backend.

* **I asked AI:** How can I obtain real time data in Flask and convert it into the DataFrame format required by the model predict function?
* **AI told me:** Use the Python `datetime` module to extract the current hour and day of the week, combine this with the latest weather data from the database, and construct a dictionary. Then convert it into a single row DataFrame using `pandas.DataFrame([data_dict])`, ensuring that the column names match those used during model training.

3. The EC2 instance has only 1GB of memory. When running backend services with model prediction logic, memory usage frequently reaches 100 percent and the server crashes.

* **I asked AI:** The EC2 instance has only 1GB of memory. How can this be resolved without upgrading the instance?
* **AI told me:** Configure Linux swap space to mitigate insufficient physical memory. It provided commands such as `sudo fallocate -l 2G /swapfile`, `sudo chmod 600 /swapfile`, `sudo mkswap /swapfile`, and `sudo swapon /swapfile`. After configuration, the system can move part of memory data to disk when RAM is exhausted, preventing process crashes.

---

## Appendix: Example Q and A

**Q: Why did I modify a file but no changes appear in VS Code?**

**A:** This situation is very common. It is similar to putting your keys in your pocket and thinking they are lost. If you cannot see changes in Source Control, there are usually three possible causes.

First, the file may not be saved. Check whether there is a solid dot next to the file name tab. If there is, it means the file is not saved. Git does not recognize unsaved files. Press Cmd and S on Mac to save the file, and the changes should appear immediately.

Second, the changes may already be committed. It is possible that the files were committed but not pushed. Check the bottom of the Source Control panel or the status bar for an upward arrow with a number. If it exists, click Sync Changes or Publish Branch.

Third, the wrong folder may be opened. If VS Code is opened at a subfolder level instead of the project root, Git may not work correctly. Open the Explorer panel and check whether project files such as Python files are visible. If only data files are shown, reopen the correct parent folder using File and then Open Folder.

If none of the above works, use the terminal and run `git status`. If it shows nothing to commit, the repository is clean. If it lists files, then the interface may not be refreshed and restarting VS Code should resolve the issue.

**Q: How can I assign tasks to teammates in Jira using email?**

**A:** To efficiently assign tasks and ensure teammates receive email notifications, follow these steps.

First, create a sprint and add issues in the backlog. Log in to the Jira project, go to Backlog, create a sprint if needed, and create issues for each teammate with clear titles.

Second, configure each task in detail. Set the assignee to the appropriate teammate, as this action triggers email notifications. Add a clear description using Markdown for readability. Set the priority and ensure the task is assigned to the correct sprint.

Third, email notifications are triggered automatically when a task is assigned or when a teammate is mentioned in a comment using the at symbol.

Fourth, you can manually copy the task link and share it through messaging tools if needed.

As a professional practice, consider using sub tasks to break down larger tasks into smaller parts such as backend, frontend, and database work. This improves clarity and progress tracking.