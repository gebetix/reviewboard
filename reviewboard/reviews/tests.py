
from reviewboard.reviews.models import Comment, \
                                       DefaultReviewer, \
                                       Group, \
                                       ReviewRequest, \
                                       ReviewRequestDraft, \
                                       Review, \
                                       Screenshot
from reviewboard.testing.testcase import TestCase
class ReviewRequestManagerTests(TestCase):
    """Tests ReviewRequestManager functions."""
    fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools',
                'test_site']
    def test_public(self):
        """Testing ReviewRequest.objects.public"""
            ReviewRequest.objects.public(
                user=User.objects.get(username="doc")), [
            "Comments Improvements",
            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements",
            "Error dialog",
            "Interdiff Revision Test",
        ])
            ReviewRequest.objects.public(status=None), [
            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements",
            "Error dialog",
            "Improved login form",
            "Interdiff Revision Test",
        ])
            ReviewRequest.objects.public(
                user=User.objects.get(username="doc"), status=None), [
            "Comments Improvements",
            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements",
            "Error dialog",
            "Improved login form",
            "Interdiff Revision Test",
        ])

    def test_public_without_private_repo_access(self):
        """Testing ReviewRequest.objects.public without access to private
        repositories
        """
        ReviewRequest.objects.all().delete()

        user = User.objects.get(username='grumpy')

        repository = self.create_repository(public=False)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        self.assertFalse(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 0)
    def test_public_with_private_repo_access(self):
        """Testing ReviewRequest.objects.public with access to private
        repositories
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        repository = self.create_repository(public=False)
        repository.users.add(user)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        self.assertTrue(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 1)
    def test_public_with_private_repo_access_through_group(self):
        """Testing ReviewRequest.objects.public with access to private
        repositories
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        group = self.create_review_group(invite_only=True)
        group.users.add(user)
        repository = self.create_repository(public=False)
        repository.review_groups.add(group)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        self.assertTrue(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 1)
    def test_public_without_private_group_access(self):
        """Testing ReviewRequest.objects.public without access to private
        group
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        group = self.create_review_group(invite_only=True)
        review_request = self.create_review_request(publish=True)
        review_request.target_groups.add(group)
        self.assertFalse(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 0)
    def test_public_with_private_group_access(self):
        """Testing ReviewRequest.objects.public with access to private
        group
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        group = self.create_review_group(invite_only=True)
        group.users.add(user)
        review_request = self.create_review_request(publish=True)
        review_request.target_groups.add(group)
        self.assertTrue(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 1)
    def test_public_with_private_repo_and_public_group(self):
        """Testing ReviewRequest.objects.public without access to private
        repositories and with access to private group
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        group = self.create_review_group()
        repository = self.create_repository(public=False)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        review_request.target_groups.add(group)
        self.assertFalse(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 0)
    def test_public_with_private_group_and_public_repo(self):
        """Testing ReviewRequest.objects.public with access to private
        group and without access to private group
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        group = self.create_review_group(invite_only=True)
        repository = self.create_repository(public=False)
        repository.users.add(user)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        review_request.target_groups.add(group)
        self.assertFalse(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 0)
    def test_public_with_private_repo_and_target_people(self):
        """Testing ReviewRequest.objects.public without access to private
        repository and user in target_people
        """
        ReviewRequest.objects.all().delete()
        user = User.objects.get(username='grumpy')
        repository = self.create_repository(public=False)
        review_request = self.create_review_request(repository=repository,
                                                    publish=True)
        review_request.target_people.add(user)
        self.assertFalse(review_request.is_accessible_by(user))
        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 0)

    def test_public_with_private_group_and_target_people(self):
        """Testing ReviewRequest.objects.public without access to private
        group and user in target_people
        """
        ReviewRequest.objects.all().delete()

        user = User.objects.get(username='grumpy')
        group = self.create_review_group(invite_only=True)

        review_request = self.create_review_request(publish=True)
        review_request.target_groups.add(group)
        review_request.target_people.add(user)
        self.assertTrue(review_request.is_accessible_by(user))

        review_requests = ReviewRequest.objects.public(user=user)
        self.assertEqual(review_requests.count(), 1)

    def test_to_group(self):
        """Testing ReviewRequest.objects.to_group"""
            ReviewRequest.objects.to_group("privgroup", None),
            ["Add permission checking for JSON API"])
            ReviewRequest.objects.to_group("privgroup", None, status=None),
            ["Add permission checking for JSON API"])
    def test_to_user_group(self):
        """Testing ReviewRequest.objects.to_user_groups"""
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_groups("doc", local_site=None),
            ["Update for cleaned_data changes",
             "Add permission checking for JSON API"])
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_groups("doc", status=None,
                local_site=None),
            ["Update for cleaned_data changes",
             "Add permission checking for JSON API"])
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_groups("doc",
                User.objects.get(username="doc"), local_site=None),
            ["Comments Improvements",
             "Update for cleaned_data changes",
             "Add permission checking for JSON API"])

    def test_to_user_directly(self):
        """Testing ReviewRequest.objects.to_user_directly"""
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_directly("doc", local_site=None),
            ["Add permission checking for JSON API",
             "Made e-mail improvements"])
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_directly("doc", status=None),
            ["Add permission checking for JSON API",
             "Made e-mail improvements",
             "Improved login form"])
        self.assertValidSummaries(
            ReviewRequest.objects.to_user_directly("doc",
                User.objects.get(username="doc"), status=None, local_site=None),
            ["Add permission checking for JSON API",
             "Made e-mail improvements",
             "Improved login form"])

    def test_from_user(self):
        """Testing ReviewRequest.objects.from_user"""
        self.assertValidSummaries(
            ReviewRequest.objects.from_user("doc", local_site=None), [])
        self.assertValidSummaries(
            ReviewRequest.objects.from_user("doc", status=None, local_site=None),
            ["Improved login form"])
            ReviewRequest.objects.from_user("doc",
                user=User.objects.get(username="doc"), status=None,
                local_site=None),
            ["Comments Improvements",
             "Improved login form"])

    def to_user(self):
        """Testing ReviewRequest.objects.to_user"""
        self.assertValidSummaries(
            ReviewRequest.objects.to_user("doc", local_site=None), [
            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements"
        ])
            ReviewRequest.objects.to_user("doc", status=None, local_site=None), [

            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements",
            "Improved login form"
        ])
            ReviewRequest.objects.to_user("doc",
                User.objects.get(username="doc"), status=None, local_site=None), [
            "Comments Improvements",
            "Update for cleaned_data changes",
            "Add permission checking for JSON API",
            "Made e-mail improvements",
            "Improved login form"
        ])
            self.assert_(summary in summaries,
                         u'summary "%s" not found in summary list' % summary)
            self.assert_(summary in r_summaries,
                         u'summary "%s" not found in review request list' %
                         summary)
    fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools',
                'test_site']
        review_request = ReviewRequest.objects.public()[0]
        response = self.client.get('/r/3/')
        self.assertEqual(request.submitter.username, 'admin')
        self.assertEqual(request.summary, 'Add permission checking for JSON API')
        self.assertEqual(request.description,
                         'Added some user permissions checking for JSON API functions.')
        self.assertEqual(request.testing_done, 'Tested some functions.')

        self.assertEqual(request.target_people.count(), 2)
        self.assertEqual(request.target_people.all()[0].username, 'doc')
        self.assertEqual(request.target_people.all()[1].username, 'dopey')

        self.assertEqual(request.target_groups.count(), 1)
        self.assertEqual(request.target_groups.all()[0].name, 'privgroup')

        self.assertEqual(request.bugs_closed, '1234, 5678, 8765, 4321')
        self.assertEqual(request.status, 'P')

        # TODO - diff
        # TODO - reviews

        self.client.logout()
        review_request = ReviewRequest.objects.get(
            summary="Add permission checking for JSON API")
        filediff = \
            review_request.diffset_history.diffsets.latest().files.all()[0]

        # Remove all the reviews on this.
        review_request.reviews.all().delete()
        main_review = Review.objects.create(review_request=review_request,
                                            user=user1)
        main_comment = main_review.comments.create(filediff=filediff,
                                                   first_line=1,
                                                   num_lines=1,
                                                   text=comment_text_1)
        reply1 = Review.objects.create(review_request=review_request,
                                       user=user1,
                                       base_reply_to=main_review,
                                       timestamp=main_review.timestamp +
                                                 timedelta(days=1))
        reply1.comments.create(filediff=filediff,
                               first_line=1,
                               num_lines=1,
                               text=comment_text_2,
                               reply_to=main_comment)
        reply2 = Review.objects.create(review_request=review_request,
                                       user=user2,
                                       base_reply_to=main_review,
                                       timestamp=main_review.timestamp +
                                                 timedelta(days=2))
        reply2.comments.create(filediff=filediff,
                               first_line=1,
                               num_lines=1,
                               text=comment_text_3,
                               reply_to=main_comment)
        comments = entry['diff_comments']
        filename = os.path.join(settings.HTDOCS_ROOT,
                                'media', 'rb', 'images', 'trophy.png')
                                              file=file)
                                              file=file)
                                              file=file)
        comments = entry['file_attachment_comments']
        comments = entry['screenshot_comments']
        self.client.logout()

    def testNewReviewRequest1(self):
        """Testing new_review_request view (uploading diffs)"""
        self.client.login(username='grumpy', password='grumpy')

        response = self.client.get('/r/new/')
        self.assertEqual(response.status_code, 200)

        testdata_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'scmtools', 'testdata')
        svn_repo_path = os.path.join(testdata_dir, 'svn_repo')

        repository = Repository(name='Subversion SVN',
                                path='file://' + svn_repo_path,
                                tool=Tool.objects.get(name='Subversion'))
        repository.save()

        diff_filename = os.path.join(testdata_dir, 'svn_makefile.diff')

        f = open(diff_filename, 'r')

        response = self.client.post('/r/new/', {
            'repository': repository.id,
            'diff_path': f,
            'basedir': '/trunk',
        })

        f.close()

        self.assertEqual(response.status_code, 302)

        r = ReviewRequest.objects.order_by('-time_added')[0]
        self.assertEqual(response['Location'],
                         'http://testserver%s' % r.get_absolute_url())

        self.assert_(datagrid)
        self.assertEqual(len(datagrid.rows), 6)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Interdiff Revision Test')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Made e-mail improvements')
        self.assertEqual(datagrid.rows[2]['object'].summary,
                         'Improved login form')
        self.assertEqual(datagrid.rows[3]['object'].summary,
                         'Error dialog')
        self.assertEqual(datagrid.rows[4]['object'].summary,
                         'Update for cleaned_data changes')
        self.assertEqual(datagrid.rows[5]['object'].summary,
                         'Add permission checking for JSON API')

        self.client.logout()
    def test_all_review_requests_with_private_review_requests(self):
        """Testing all_review_requests view with private review requests"""
        ReviewRequest.objects.all().delete()

        user = User.objects.get(username='grumpy')

        # These are public
        self.create_review_request(summary='Test 1', publish=True)
        self.create_review_request(summary='Test 2', publish=True)

        repository1 = self.create_repository(public=False)
        repository1.users.add(user)
        self.create_review_request(summary='Test 3',
                                   repository=repository1,
                                   publish=True)

        group1 = self.create_review_group(invite_only=True)
        group1.users.add(user)
        review_request = self.create_review_request(summary='Test 4',
                                                    publish=True)
        review_request.target_groups.add(group1)

        # These are private
        repository2 = self.create_repository(public=False)
        self.create_review_request(summary='Test 5',
                                   repository=repository2,
                                   publish=True)

        group2 = self.create_review_group(invite_only=True)
        review_request = self.create_review_request(summary='Test 6',
                                                    publish=True)
        review_request.target_groups.add(group2)

        # Log in and check what we get.
        self.client.login(username='grumpy', password='grumpy')

        response = self.client.get('/r/')
        self.assertEqual(response.status_code, 200)

        datagrid = self.getContextVar(response, 'datagrid')
        self.assertTrue(datagrid)
        self.assertEqual(len(datagrid.rows), 4)
        self.assertEqual(datagrid.rows[0]['object'].summary, 'Test 4')
        self.assertEqual(datagrid.rows[1]['object'].summary, 'Test 3')
        self.assertEqual(datagrid.rows[2]['object'].summary, 'Test 2')
        self.assertEqual(datagrid.rows[3]['object'].summary, 'Test 1')

        self.assert_(datagrid)
        self.assert_(datagrid)
        self.assert_(datagrid)
        self.assertEqual(len(datagrid.rows), 4)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Made e-mail improvements')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Update for cleaned_data changes')
        self.assertEqual(datagrid.rows[2]['object'].summary,
                         'Comments Improvements')
        self.assertEqual(datagrid.rows[3]['object'].summary,
                         'Add permission checking for JSON API')

        self.client.logout()
        self.assert_(datagrid)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Interdiff Revision Test')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Add permission checking for JSON API')

        self.client.logout()
        self.assert_(datagrid)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Made e-mail improvements')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Add permission checking for JSON API')
        self.client.logout()
    def test_dashboard_to_group_with_joined_groups(self):
        """Testing dashboard view with to-group and joined groups"""
        self.client.login(username='doc', password='doc')
        group = Group.objects.get(name='devgroup')
        group.users.add(User.objects.get(username='doc'))
        self.assert_(datagrid)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Update for cleaned_data changes')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Comments Improvements')
        self.client.logout()
    def test_dashboard_to_group_with_unjoined_group(self):
        """Testing dashboard view with to-group and unjoined group"""
        self.client.login(username='doc', password='doc')
        group = self.create_review_group(name='new-group')
        review_request = self.create_review_request(summary='Test 1',
        review_request.target_groups.add(group)
        response = self.client.get('/dashboard/',
                                   {'view': 'to-group',
                                    'group': 'new-group'})
        self.assertEqual(response.status_code, 404)
    def testDashboardSidebar(self):
        """Testing dashboard view (to-group devgroup)"""
        self.client.login(username='doc', password='doc')
        user = User.objects.get(username='doc')
        profile = user.get_profile()
        local_site = None
        datagrid = self.getContextVar(response, 'datagrid')
        self.assertEqual(
            datagrid.counts['outgoing'],
            ReviewRequest.objects.from_user(
                user, user, local_site=local_site).count())
        self.assertEqual(
            datagrid.counts['incoming'],
            ReviewRequest.objects.to_user(user, local_site=local_site).count())
        self.assertEqual(
            datagrid.counts['to-me'],
            ReviewRequest.objects.to_user_directly(
                user, local_site=local_site).count())
        self.assertEqual(
            datagrid.counts['starred'],
            profile.starred_review_requests.public(
                user, local_site=local_site).count())
        self.assertEqual(datagrid.counts['mine'],
            ReviewRequest.objects.from_user(
                user, user, None, local_site=local_site).count())
        self.assertEqual(datagrid.counts['groups']['devgroup'],
            ReviewRequest.objects.to_group(
                'devgroup', local_site=local_site).count())
        self.assertEqual(datagrid.counts['groups']['privgroup'],
            ReviewRequest.objects.to_group(
                'privgroup', local_site=local_site).count())

        self.client.logout()
        response = self.client.get('/r/8/diff/1-2/')
        self.assertEqual(self.getContextVar(response, 'num_diffs'), 3)
        self.assert_(files)
        self.assertEqual(files[0]['depot_filename'],
                         '/trunk/reviewboard/TESTING')
        self.assert_('fragment' in files[0])
        self.assert_('interfilediff' in files[0])
        self.assertEqual(files[1]['depot_filename'],
                         '/trunk/reviewboard/settings_local.py.tmpl')
        self.assert_('fragment' not in files[1])
        self.assert_('interfilediff' in files[1])
        response = self.client.get('/r/8/diff/2-3/')
        self.assertEqual(self.getContextVar(response, 'num_diffs'), 3)
        self.assert_(files)
        self.assertEqual(files[0]['depot_filename'],
                         '/trunk/reviewboard/NEW_FILE')
        self.assert_('fragment' in files[0])
        self.assert_('interfilediff' in files[0])
        self.assert_(datagrid)
        self.assertEqual(datagrid.rows[0]['object'].summary,
                         'Improved login form')
        self.assertEqual(datagrid.rows[1]['object'].summary,
                         'Comments Improvements')

        self.client.logout()
        review_request = ReviewRequest.objects.get(
            summary="Add permission checking for JSON API")
        filediff = \
            review_request.diffset_history.diffsets.latest().files.all()[0]
        review = Review(review_request=review_request, user=user)
        review.save()

        comment = review.comments.create(filediff=filediff, first_line=1)
        comment.text = 'This is a test'
        comment.issue_opened = True
        comment.issue_status = Comment.OPEN
        comment.num_lines = 1
        comment.save()

    fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools']
        self.assert_("summary" in fields)
        self.assert_("description" in fields)
        self.assert_("testing_done" in fields)
        self.assert_("branch" in fields)
        self.assert_("bugs_closed" in fields)
        return ReviewRequestDraft.create(ReviewRequest.objects.get(
            summary="Add permission checking for JSON API"))
    def testLongBugNumbers(self):
    def testNoSummary(self):
    fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools']
        review_request = ReviewRequest.objects.get(
            summary="Add permission checking for JSON API")
        filediff = \
            review_request.diffset_history.diffsets.latest().files.all()[0]
        review = Review(review_request=review_request, user=user)
        review.body_top = body_top
        review.save()
        master_review = review

        comment = review.comments.create(filediff=filediff, first_line=1)
        comment.text = comment_text_1
        comment.num_lines = 1
        comment.save()
        review = Review(review_request=review_request, user=user)
        review.save()

        comment = review.comments.create(filediff=filediff, first_line=1)
        comment.text = comment_text_2
        comment.num_lines = 1
        comment.save()
        review = Review(review_request=review_request, user=user)
        review.body_bottom = body_bottom
        review.save()

        comment = review.comments.create(filediff=filediff, first_line=1)
        comment.text = comment_text_3
        comment.num_lines = 1
        comment.save()
        self.assert_(review)
        self.assert_(len(default_reviewers) == 2)
        self.assert_(default_reviewer1 in default_reviewers)
        self.assert_(default_reviewer2 in default_reviewers)
        self.assert_(len(default_reviewers) == 1)
        self.assert_(default_reviewer2 in default_reviewers)
        default_reviewers = DefaultReviewer.objects.for_repository(None, test_site)
        self.assert_(len(default_reviewers) == 1)
        self.assert_(default_reviewer1 in default_reviewers)
        self.assert_(len(default_reviewers) == 1)
        self.assert_(default_reviewer2 in default_reviewers)
    fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools',
                'test_site']
        review_request = self._get_review_request()
        review_request = self._get_review_request()
        review_request = self._get_review_request()
        review_request = self._get_review_request()
        review_request.save()

        review_request = self._get_review_request()
        review_request.save()

        review_request = self._get_review_request()
        review_request.save()

    def _get_review_request(self, local_site=None):
        # Get a review request and clear out the reviewers.
        review_request = ReviewRequest.objects.public(local_site=local_site)[0]
        review_request.target_people.clear()
        review_request.target_groups.clear()
        return review_request
