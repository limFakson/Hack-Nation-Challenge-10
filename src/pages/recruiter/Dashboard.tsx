import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Briefcase, Users, TrendingUp, Eye, Clock, CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";

export default function RecruiterDashboard() {
  const stats = [
    { title: "Active Jobs", value: "12", icon: Briefcase, change: "+2 this week" },
    { title: "Total Candidates", value: "248", icon: Users, change: "+18 this week" },
    { title: "Successful Hires", value: "8", icon: CheckCircle, change: "+3 this month" },
    { title: "Match Rate", value: "94%", icon: TrendingUp, change: "+5% this month" },
  ];

  const recentJobs = [
    {
      id: 1,
      title: "Senior Frontend Developer",
      department: "Engineering",
      status: "active",
      candidates: 23,
      posted: "2 days ago",
      score: 95
    },
    {
      id: 2,
      title: "Product Manager",
      department: "Product",
      status: "active",
      candidates: 18,
      posted: "5 days ago",
      score: 87
    },
    {
      id: 3,
      title: "UX Designer",
      department: "Design",
      status: "filled",
      candidates: 31,
      posted: "1 week ago",
      score: 92
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">Recruiter Dashboard</h1>
              <p className="text-muted-foreground mt-1">Manage your jobs and find top talent</p>
            </div>
            <Link to="/recruiter/jobs/new">
              <Button variant="hero" size="lg">
                <Plus className="w-5 h-5 mr-2" />
                Post New Job
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <Card key={index} className="border-0 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                    <p className="text-3xl font-bold">{stat.value}</p>
                    <p className="text-sm text-success">{stat.change}</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <stat.icon className="w-6 h-6 text-primary" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Jobs */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recent Job Postings</CardTitle>
                    <CardDescription>Manage and track your active job listings</CardDescription>
                  </div>
                  <Link to="/recruiter/jobs">
                    <Button variant="outline">View All</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentJobs.map((job) => (
                    <div key={job.id} className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold">{job.title}</h3>
                        <Badge variant={job.status === 'active' ? 'default' : 'secondary'}>
                          {job.status}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-3">{job.department}</p>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center space-x-4">
                          <span className="flex items-center">
                            <Users className="w-4 h-4 mr-1" />
                            {job.candidates} candidates
                          </span>
                          <span className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {job.posted}
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-success font-medium">{job.score}% match</span>
                          <Link to={`/recruiter/jobs/${job.id}/candidates`}>
                            <Button variant="outline" size="sm">
                              <Eye className="w-4 h-4 mr-1" />
                              View
                            </Button>
                          </Link>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="space-y-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Link to="/recruiter/jobs/new" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <Plus className="w-4 h-4 mr-2" />
                    Post New Job
                  </Button>
                </Link>
                <Link to="/recruiter/candidates" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <Users className="w-4 h-4 mr-2" />
                    Browse Candidates
                  </Button>
                </Link>
                <Link to="/recruiter/analytics" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    View Analytics
                  </Button>
                </Link>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-gradient-to-r from-primary/5 to-accent/5">
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-white rounded-lg border">
                    <p className="text-sm font-medium">Top Skill in Demand</p>
                    <p className="text-lg font-bold text-primary">React.js</p>
                  </div>
                  <div className="p-3 bg-white rounded-lg border">
                    <p className="text-sm font-medium">Best Time to Post</p>
                    <p className="text-lg font-bold text-primary">Tuesday 10AM</p>
                  </div>
                  <div className="p-3 bg-white rounded-lg border">
                    <p className="text-sm font-medium">Avg. Response Time</p>
                    <p className="text-lg font-bold text-success">2.3 days</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}