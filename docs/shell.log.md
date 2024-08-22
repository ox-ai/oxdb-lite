# ox_db shell

## base cmd :

```
oxdb = Oxdb("hosted")

oxdb.info()
oxdb.doc.info()
oxdb.get_db(db_name)
oxdb.doc.get_doc(doc_name)
oxdb.doc.push(**data)
oxdb.doc.pull(**data)
oxdb.doc.search(**data)
```

### > shell session :

- initiate a shell session in terminall for quick access

<pre>                                                                                                           
<font color="#5EBDAB">┌──(</font><font color="#277FFF"><b>lokesh㉿kali</b></font><font color="#5EBDAB">)-[</font><b>~</b><font color="#5EBDAB">]</font>
<font color="#5EBDAB">└─</font><font color="#277FFF"><b>$</b></font> <font color="#49AEE6">oxdb.shell</font>                                     
oxdb&gt; search &quot;implementation plan&quot;
oxdb : 
{&apos;data&apos;: [&apos;data-1&apos;,
          &apos;need to implement pdfsearch db with ui&apos;,
          &apos;{&quot;datas&quot;: [&quot;project-queue&quot;, &quot;priority is db&quot;]}&apos;]}
</pre>


<pre><font color="#5EBDAB">┌──(</font><font color="#277FFF"><b>lokesh㉿kali</b></font><font color="#5EBDAB">)-[</font><b>~</b><font color="#5EBDAB">]</font>
<font color="#5EBDAB">└─</font><font color="#277FFF"><b>$</b></font> <font color="#49AEE6">oxdb.shell</font>
oxdb&gt; info
oxdb : 
{&apos;db&apos;: &apos;hosted&apos;,
 &apos;db_path&apos;: &apos;/home/lokesh/ox-db/hosted.oxdb&apos;,
 &apos;doc_list&apos;: [&apos;log-[18_08_2024]&apos;, &apos;log-[20_08_2024]&apos;, &apos;log-[19_08_2024]&apos;],
 &apos;doc_name&apos;: &apos;log-[20_08_2024]&apos;,
 &apos;doc_path&apos;: &apos;/home/lokesh/ox-db/hosted.oxdb/log-[20_08_2024]&apos;,
 &apos;vec_model&apos;: &apos;sentence-transformers/all-MiniLM-L6-v2&apos;}
oxdb&gt; ^C
Exiting shell...
                      </pre>
to start ox-db shell run below cmd refere [shell.log.md](./docs/shell.log.md) for further detials

### Linux , macos and Windows

- cmd to initiate terminal session which can intract directly to ox-db

```bash
oxdb.shell
```

- on terminal access : to send db query to server with out starting a session
- through terminal start the server then execute `oxdb.shell "oxdb query"`
- refere [ox-db server](#ox-db-server) to start server

```bash
oxdb.shell "oxdb query"
```

- if path not correctly assigned due too sudo or admin access use below cmd

```bash
python -m ox_db.shell.log
```
