import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { User, Briefcase, Star, TrendingUp, Clock, MapPin, Building2 } from "lucide-react";
import { Link } from "react-router-dom";

export default function TalentDashboard() {
  const profileScore = 85;
  
  const stats = [
    { title: "Profile Views", value: "156", icon: User, change: "+12 this week" },
    { title: "Job Matches", value: "8", icon: Briefcase, change: "+3 new" },
    { title: "Skill Score", value: "92%", icon: Star, change: "+5% this month" },
    { title: "Response Rate", value: "94%", icon: TrendingUp, change: "Excellent" },
  ];

  const jobMatches = [
    {
      id: 1,
      title: "Senior Frontend Developer",
      company: "TechCorp Inc.",
      location: "San Francisco, CA",
      salary: "$120k - $150k",
      matchScore: 95,
      posted: "2 days ago",
      type: "Full-time"
    },
    {
      id: 2,
      title: "React Developer",
      company: "StartupXYZ",
      location: "Remote",
      salary: "$100k - $130k",
      matchScore: 87,
      posted: "1 week ago",
      type: "Contract"
    },
    {
      id: 3,
      title: "Full Stack Engineer",
      company: "InnovateLabs",
      location: "New York, NY",
      salary: "$110k - $140k",
      matchScore: 82,
      posted: "3 days ago",
      type: "Full-time"
    },
  ];

  const challenges = [
    { title: "React Advanced Patterns", difficulty: "Expert", points: 500, duration: "2 hours" },
    { title: "JavaScript Algorithms", difficulty: "Intermediate", points: 300, duration: "1 hour" },
    { title: "CSS Flexbox Mastery", difficulty: "Beginner", points: 200, duration: "45 min" },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold">Talent Dashboard</h1>
              <p className="text-muted-foreground mt-1">Track your opportunities and grow your skills</p>
            </div>
            <Link to="/talent/profile">
              <Button variant="hero" size="lg">
                <User className="w-5 h-5 mr-2" />
                Update Profile
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Score */}
        <Card className="border-0 shadow-lg mb-8 bg-gradient-to-r from-primary/5 to-accent/5">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold mb-2">Profile Completeness</h3>
                <p className="text-muted-foreground mb-4">Complete your profile to get better matches</p>
                <Progress value={profileScore} className="w-64" />
                <p className="text-sm text-muted-foreground mt-2">{profileScore}% complete</p>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">{profileScore}%</div>
                <p className="text-sm text-success">+5% this week</p>
              </div>
            </div>
          </CardContent>
        </Card>

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
          {/* Job Matches */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Job Matches</CardTitle>
                    <CardDescription>Jobs that match your skills and preferences</CardDescription>
                  </div>
                  <Link to="/talent/jobs">
                    <Button variant="outline">View All</Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {jobMatches.map((job) => (
                    <div key={job.id} className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold">{job.title}</h3>
                        <Badge variant="default" className="bg-success">
                          {job.matchScore}% match
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-3">
                        <span className="flex items-center">
                          <Building2 className="w-4 h-4 mr-1" />
                          {job.company}
                        </span>
                        <span className="flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {job.location}
                        </span>
                        <Badge variant="secondary">{job.type}</Badge>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 text-sm">
                          <span className="font-medium text-primary">{job.salary}</span>
                          <span className="flex items-center text-muted-foreground">
                            <Clock className="w-4 h-4 mr-1" />
                            {job.posted}
                          </span>
                        </div>
                        <Link to={`/talent/jobs/${job.id}`}>
                          <Button variant="outline" size="sm">
                            View Details
                          </Button>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Link to="/talent/profile" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <User className="w-4 h-4 mr-2" />
                    Update Profile
                  </Button>
                </Link>
                <Link to="/talent/jobs" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <Briefcase className="w-4 h-4 mr-2" />
                    Browse Jobs
                  </Button>
                </Link>
                <Link to="/talent/challenges" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <Star className="w-4 h-4 mr-2" />
                    Take Challenges
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Skill Challenges */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>Skill Challenges</CardTitle>
                <CardDescription>Boost your profile score</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {challenges.map((challenge, index) => (
                    <div key={index} className="p-3 border rounded-lg hover:bg-muted/50 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-medium text-sm">{challenge.title}</h4>
                        <Badge variant="outline" className="text-xs">
                          +{challenge.points} pts
                        </Badge>
                      </div>
                      <div className="flex justify-between text-xs text-muted-foreground">
                        <span>{challenge.difficulty}</span>
                        <span>{challenge.duration}</span>
                      </div>
                    </div>
                  ))}
                </div>
                <Link to="/talent/challenges" className="block mt-4">
                  <Button variant="outline" className="w-full" size="sm">
                    View All Challenges
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}