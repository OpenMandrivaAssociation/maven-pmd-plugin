Name:           maven-pmd-plugin
Version:        2.5
Release:        5
Summary:        Maven PMD Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-pmd-plugin/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        maven-pmd-plugin-depmap.xml

BuildArch: noarch

BuildRequires: pmd
BuildRequires: java-devel >= 0:1.6.0
BuildRequires: maven
BuildRequires: maven-plugin-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit4
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-archiver
BuildRequires: plexus-archiver
BuildRequires: apache-commons-lang
BuildRequires: plexus-resources
BuildRequires: plexus-utils
BuildRequires: junit
Requires: maven
Requires: plexus-utils
Requires: maven-plugin-testing-harness
Requires: pmd
Requires: junit
Requires:       jpackage-utils
Requires:       java
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

Provides:       maven2-plugin-pmd = %{version}-%{release}
Obsoletes:      maven2-plugin-pmd <= 0:2.0.8

%description
A Maven plugin for the PMD toolkit, that produces a report on both code rule 
violations and detected copy and paste fragments, as well as being able to 
fail the build based on these metrics.
  

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q 

%build
mvn-rpmbuild \
        -Dmaven.local.depmap.file=%{SOURCE1} \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.apache.maven.plugins maven-pmd-plugin %{version} JPP maven-pmd-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}/

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

