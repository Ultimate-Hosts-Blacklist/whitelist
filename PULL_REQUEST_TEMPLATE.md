Introduction of:

*Please list here the list of sub-domains that you introduced.*

* `example.org`
  * If an explanation about the whitelisting request exist, please put it here.
  * If there is a documentation link about the owner or the trust page of the owner, please put it here.
* `test.example.org`
  * If an explanation about the whitelisting exist request, please put it here.
  * If there is a documentation link about the owner or the trust page of the owner, please put it here.
  
*Please put here a wiki page (if exist) which is relevant with your whitelisting request.*


# Checklist

*Please complete by replacing `[ ]` to `[x]` if it is checked.*

* [ ] Are the changed made under `domains.list`?
* [ ] Does the commit(s) message(s) follow one of the following templates ?
  * Note: We impose this in order to help us get back if there is a problem in the future.
  * Note: We do not care if you respect the punctuation, we just except that you follow the format.
  
  ```
  Introduction of `example.org`.
  ```
  ```
  Introduction of `example.org`.
  
  This patch fix #xyz.
  ```
  ```
  Introduction of several `example.org` subdomains.
  
    * `test.example.org`
    * `hello_world.example.org`
    * `world_hello.example.org`
    
  This patch fix #xyz.
  ```
  ```
  Deletion of `example.org`
  ```
  ```
  Deletion of `example.org`
  
  This domain is now used for phishing of google and facebook.
  
  This patch fix #xyz
  ```
* [ ] Is there a commit per domain or a commit per subdomains of the same domain ?
  * Note: We impose this in order to help us get back if there is a problem in the future.
* [ ] (optional but recommended) Is your commit signed ?
  * Note: More info about commit signature can be found [here](https://help.github.com/articles/signing-commits/).
* [ ] (optional) Is `domains.list` sorted with the help of `:sort u | sort i | wq` from inside `vim`?
* [ ] Is `domains.list` sorted ?
